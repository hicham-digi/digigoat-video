<#
.SYNOPSIS
  Prémontage vertical à partir de rushes : vérifications, orientation, conversion, segments,
  assemblage, musique et texte optionnels, contrôles techniques et rapport.

.DESCRIPTION
  Windows PowerShell 5.1 + ffmpeg/ffprobe déjà installés. Rien n'est installé ni téléchargé.
  Les rushes ne sont jamais modifiés. Chaque exécution crée un NOUVEAU dossier de sortie.
  Mode d'emploi : scripts/README.md · Procédure : sops/procedure-premontage.md

.EXAMPLE
  powershell -NoProfile -ExecutionPolicy Bypass -File scripts\premontage.ps1 `
    -Rushes "D:\rushes" -Brief clients\x\brief.md -Client clients\x -Sortie "D:\sorties" `
    -Plan clients\x\plan.csv -Orientation anti-horaire
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)][string]$Rushes,
  [Parameter(Mandatory = $true)][string]$Brief,
  [Parameter(Mandatory = $true)][string]$Client,
  [Parameter(Mandatory = $true)][string]$Sortie,
  [string]$Musique = '',
  [string]$Plan = '',
  [ValidateSet('demander', 'aucune', 'anti-horaire', 'horaire', 'recadrer-centre')][string]$Orientation = 'demander',
  [string]$OrientationParRush = '',
  [string]$Texte = '',
  [string]$PoliceTexte = '',
  [double]$TexteTaille = 0,
  [double]$TexteCentreY = -1,
  [double]$TexteInterligne = 0,
  [double]$TexteOmbreFlou = -1,
  [double]$TexteOmbreDecalage = -1,
  [string]$Compteur = '',
  [double]$CompteurCentreY = 0.585,
  [double]$DepartMusique = -1,
  [double]$FonduEntree = -1,
  [double]$FonduSortie = -1,
  [double]$GainMusiqueDb = 0,
  [double]$DureePlan = 0,
  [string]$DureeCible = '',
  [ValidateSet('couper', 'garder')][string]$SonOrigine = 'couper',
  [string]$Transcription = '',
  [switch]$Auto
)

$ErrorActionPreference = 'Stop'
$ci = [Globalization.CultureInfo]::InvariantCulture
$utf8 = New-Object System.Text.UTF8Encoding($false)
$script:cmdLog = New-Object System.Collections.Generic.List[string]
$script:paramRows = New-Object System.Collections.Generic.List[object]
$script:checks = New-Object System.Collections.Generic.List[object]   # Etat;Libelle
$script:todo = New-Object System.Collections.Generic.List[string]     # a verifier par une personne
$script:warnings = New-Object System.Collections.Generic.List[string]

# ------------------------------------------------------------------ utilitaires
function Fmt([double]$d) { return $d.ToString('0.###', $ci) }
function Say([string]$m) { Write-Host $m }
function Add-Check([string]$etat, [string]$msg) { $script:checks.Add([pscustomobject]@{ Etat = $etat; Msg = $msg }); Say ("  [{0}] {1}" -f $etat, $msg) }
function Add-Todo([string]$msg) { if (-not $script:todo.Contains($msg)) { $script:todo.Add($msg) } }
function Get-Slug([string]$s) {
  $n = $s.Normalize([Text.NormalizationForm]::FormD)
  $n = [regex]::Replace($n, '\p{Mn}', '')
  $n = [regex]::Replace($n.ToLowerInvariant(), '[^a-z0-9]+', '-').Trim('-')
  if ($n.Length -gt 40) { $n = $n.Substring(0, 40).Trim('-') }
  if ($n.Length -eq 0) { $n = 'essai' }
  return $n
}
function Quote-Arg([string]$a) {
  if ($a.Length -gt 0 -and $a -notmatch '[\s"]') { return $a }
  $sb = New-Object System.Text.StringBuilder
  [void]$sb.Append('"')
  $bs = 0
  foreach ($c in $a.ToCharArray()) {
    if ($c -eq [char]92) { $bs++ }
    elseif ($c -eq [char]34) { [void]$sb.Append([char]92, $bs * 2 + 1); [void]$sb.Append([char]34); $bs = 0 }
    else { if ($bs -gt 0) { [void]$sb.Append([char]92, $bs); $bs = 0 }; [void]$sb.Append($c) }
  }
  if ($bs -gt 0) { [void]$sb.Append([char]92, $bs * 2) }
  [void]$sb.Append('"')
  return $sb.ToString()
}
# Lance un programme sans passer par le mecanisme d'erreurs de PowerShell ; journalise la commande exacte.
function Invoke-Tool([string]$exe, [string[]]$arguments, [string]$workdir = '', [switch]$NoLog) {
  $line = (Split-Path $exe -Leaf) + ' ' + (($arguments | ForEach-Object { Quote-Arg $_ }) -join ' ')
  if (-not $NoLog) { $script:cmdLog.Add($line) }
  $psi = New-Object System.Diagnostics.ProcessStartInfo
  $psi.FileName = $exe
  $psi.Arguments = (($arguments | ForEach-Object { Quote-Arg $_ }) -join ' ')
  $psi.UseShellExecute = $false
  $psi.RedirectStandardOutput = $true
  $psi.RedirectStandardError = $true
  $psi.CreateNoWindow = $true
  $psi.StandardOutputEncoding = [Text.Encoding]::UTF8
  $psi.StandardErrorEncoding = [Text.Encoding]::UTF8
  if ($workdir) { $psi.WorkingDirectory = $workdir }
  $p = [System.Diagnostics.Process]::Start($psi)
  $tOut = $p.StandardOutput.ReadToEndAsync()
  $tErr = $p.StandardError.ReadToEndAsync()
  $p.WaitForExit()
  return [pscustomobject]@{ Code = $p.ExitCode; Out = $tOut.Result; Err = $tErr.Result }
}
function Invoke-Ffmpeg([string[]]$arguments, [string]$label, [string]$workdir = '') {
  $r = Invoke-Tool $script:ffmpeg (@('-v', 'error', '-y') + $arguments) $workdir
  if ($r.Code -ne 0) { throw ("ffmpeg a échoué ({0}) : {1}" -f $label, $r.Err.Trim()) }
  return $r
}
function Get-Probe([string]$file) {
  $r = Invoke-Tool $script:ffprobe @('-v', 'error', '-print_format', 'json', '-show_format', '-show_streams', '--', $file) '' -NoLog
  if ($r.Code -ne 0 -or -not $r.Out.Trim()) { return $null }
  return ($r.Out | ConvertFrom-Json)
}
function Parse-Fps([string]$s) { if ($s -match '^(\d+)/(\d+)$' -and [double]$Matches[2] -ne 0) { return [double]$Matches[1] / [double]$Matches[2] } else { return 0 } }
function Esc-FilterPath([string]$p) { return ($p -replace '\\', '/') -replace ':', '\:' }
function Esc-Label([string]$s) { return ($s -replace '[^A-Za-z0-9_.\-]', '_') }

# ------------------------------------------------------------------ parametres client
function Get-ClientValue([string]$key, $default) {
  if ($script:cfg -and $script:cfg.parametres -and ($script:cfg.parametres.PSObject.Properties.Name -contains $key)) {
    $p = $script:cfg.parametres.$key
    return [pscustomobject]@{ Valeur = $p.valeur; Statut = $p.statut; Source = 'paramètres du client' }
  }
  return [pscustomobject]@{ Valeur = $default; Statut = 'défaut du script'; Source = 'défaut du script' }
}
function Resolve-Param([string]$nom, [string]$cliName, $cliValue, [string]$clientKey, $default, [switch]$Unused) {
  if ($cliName -and $PSBoundParameters.ContainsKey('cliValue') -and $null -ne $cliValue -and $script:BoundCli.ContainsKey($cliName)) {
    $v = $cliValue; $src = 'ligne de commande'; $st = 'choix de cet essai'
  }
  else {
    $c = Get-ClientValue $clientKey $default
    $v = $c.Valeur; $src = $c.Source; $st = $c.Statut
  }
  $script:paramRows.Add([pscustomobject]@{ Nom = $nom; Valeur = "$v"; Source = $src; Statut = $st })
  return $v
}

# ------------------------------------------------------------------ analyse musicale
function Get-MusicAnalysis([string]$file, [double]$dur, [double[]]$cuts, [double]$searchMax, [double]$forced = -1) {
  $T = [math]::Ceiling($searchMax + $dur + 2)
  $envPath = Join-Path $script:tmp 'env.txt'
  if (Test-Path -LiteralPath $envPath) { Remove-Item -LiteralPath $envPath -Force }
  $af = 'aresample=22050,asetnsamples=n=441:p=0,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=env.txt'
  [void](Invoke-Ffmpeg @('-t', (Fmt $T), '-i', $file, '-af', $af, '-f', 'null', 'NUL') 'analyse de la musique' $script:tmp)
  $vals = New-Object System.Collections.Generic.List[double]
  foreach ($l in [IO.File]::ReadLines($envPath)) {
    $i = $l.IndexOf('RMS_level=')
    if ($i -ge 0) {
      $s = $l.Substring($i + 10).Trim()
      $d = 0.0
      if ([double]::TryParse($s, [Globalization.NumberStyles]::Float, $ci, [ref]$d)) { $vals.Add([math]::Max($d, -120.0)) } else { $vals.Add(-120.0) }
    }
  }
  $n = $vals.Count
  if ($n -lt 100) { throw "Analyse de la musique impossible (trop peu de données : $n)." }
  $rms = $vals.ToArray()
  $ps = New-Object 'double[]' ($n + 1)
  for ($i = 0; $i -lt $n; $i++) { $ps[$i + 1] = $ps[$i] + $rms[$i] }
  $mean = { param($a, $b) $a = [math]::Max(0, $a); $b = [math]::Min($n, $b); if ($b -le $a) { return -120.0 }; return ($ps[$b] - $ps[$a]) / ($b - $a) }
  # attaques : hausse >= 6 dB en 20 ms
  $att = New-Object System.Collections.Generic.List[double]
  for ($i = 2; $i -lt $n - 2; $i++) {
    $o = $rms[$i] - $rms[$i - 1]
    if ($o -ge 6.0 -and $o -ge ($rms[$i - 1] - $rms[$i - 2]) -and $o -ge ($rms[$i + 1] - $rms[$i])) {
      $t = $i * 0.02
      if ($att.Count -eq 0 -or ($t - $att[$att.Count - 1]) -gt 0.15) { $att.Add($t) }
    }
  }
  $valid = New-Object System.Collections.Generic.List[double]
  foreach ($t in $att) {
    if ($t -gt $searchMax) { break }
    $i = [int][math]::Round($t / 0.02)
    if ($t -gt 0.4) {
      $prev = & $mean ($i - 15) ($i - 1)
      $cur = & $mean ($i + 2) ($i + 17)
      if (($cur - $prev) -lt 8.0) { continue }
    }
    $s = [math]::Max(0.0, $t - 0.04)
    if (($s + $dur) -gt ($n * 0.02)) { continue }
    $ok = $true
    for ($k = $s; $k -lt ($s + $dur - 0.5); $k += 0.5) {
      $a = [int][math]::Round($k / 0.02)
      if ((& $mean $a ($a + 25)) -lt -42.0) { $ok = $false; break }
    }
    if ($ok) { $valid.Add([math]::Round($s, 2)) }
  }
  $res = [ordered]@{}
  if ($valid.Count -gt 0) {
    $s = $valid[0]
    $res.Raison = "Première attaque nette venant d'un creux sonore dont la fenêtre de $(Fmt $dur) s ne contient aucun quasi-silence (seuil -42 dB sur 0,5 s)."
    $res.Net = $true
    $res.Alternatives = @($valid | Select-Object -Skip 1 -First 3)
  }
  else {
    $s = 0.0
    for ($i = 0; $i -lt ($n - 25); $i++) { if ((& $mean $i ($i + 25)) -ge -35.0) { $s = [math]::Round($i * 0.02, 2); break } }
    $res.Raison = "Aucune attaque nette trouvée dans les $(Fmt $searchMax) premières secondes : départ au premier son soutenu. À vérifier à l'écoute."
    $res.Net = $false
    $res.Alternatives = @()
  }
  # Départ imposé (-DepartMusique) : on garde ce départ, mais on analyse la fenêtre et la fin à PARTIR de lui.
  if ($forced -ge 0) {
    $s = [math]::Round($forced, 2)
    $okF = $true
    for ($k = $s; $k -lt ($s + $dur - 0.5); $k += 0.5) { $a = [int][math]::Round($k / 0.02); if ((& $mean $a ($a + 25)) -lt -42.0) { $okF = $false; break } }
    $net = $false; foreach ($t in $att) { if ($t -ge $s -and $t -le ($s + 0.1)) { $net = $true; break } }
    $res.Net = $net
    $res.Raison = "Départ imposé par -DepartMusique ($(Fmt $s) s). " + $(if ($okF) { "La fenêtre de $(Fmt $dur) s ne contient aucun quasi-silence (seuil -42 dB sur 0,5 s)." } else { 'ATTENTION : la fenêtre contient un quasi-silence (sous -42 dB).' })
    $res.FenetreOK = $okF
  }
  $res.Depart = $s
  $e0 = [int][math]::Round(($s + $dur - 1.5) / 0.02); $e1 = [int][math]::Round(($s + $dur) / 0.02)
  $fin = & $mean $e0 $e1
  $blocs = @()
  for ($k = $s; $k -lt ($s + $dur - 0.5); $k += 0.5) { $a = [int][math]::Round($k / 0.02); $blocs += (& $mean $a ($a + 25)) }
  $sorted = $blocs | Sort-Object
  $med = $sorted[[int][math]::Floor($sorted.Count / 2)]
  $res.NiveauFin = [math]::Round($fin, 1)
  $res.NiveauMedian = [math]::Round($med, 1)
  $res.FonduEntree = $(if ($res.Net -and $s -gt 0.3) { 0.02 } else { 0.15 })
  $res.FonduSortie = $(if ($fin -le ($med - 12)) { 1.0 } else { 2.0 })
  # alignement indicatif attaques / coupes
  $hits = @()
  foreach ($c in $cuts) { foreach ($a in $att) { $d = ($a - $s) - $c; if ([math]::Abs($d) -le 0.10) { $hits += ("{0:0.00}s({1:+0.00;-0.00})" -f $c, $d); break } } }
  $res.Alignement = "{0} coupe(s) sur {1} à moins de 0,10 s d'une attaque : {2}" -f $hits.Count, $cuts.Count, $(if ($hits.Count) { $hits -join ' ' } else { 'aucune' })
  return [pscustomobject]$res
}

# ------------------------------------------------------------------ texte (overlay)
function Get-TextLines([string]$texte, [string]$fontFile, [double]$size, [double]$maxW) {
  if ($texte.Contains('|')) { return @($texte.Split('|') | ForEach-Object { $_.Trim() } | Where-Object { $_ }) }
  Add-Type -AssemblyName System.Drawing
  $pfc = New-Object System.Drawing.Text.PrivateFontCollection
  $pfc.AddFontFile($fontFile)
  $bmp = New-Object System.Drawing.Bitmap 10, 10
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $f = New-Object System.Drawing.Font($pfc.Families[0], [single]100, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
  $fmt = [System.Drawing.StringFormat]::GenericTypographic
  $w = { param($t) $g.MeasureString($t, $f, 20000, $fmt).Width * $size / 100.0 }
  $full = & $w $texte
  $result = @($texte)
  if ($full -gt $maxW) {
    $best = $null; $bestMax = [double]::MaxValue
    for ($i = 0; $i -lt $texte.Length; $i++) {
      if ($texte[$i] -eq ' ') {
        $a = $texte.Substring(0, $i).Trim(); $b = $texte.Substring($i + 1).Trim()
        $m = [math]::Max((& $w $a), (& $w $b))
        if ($m -lt $bestMax) { $bestMax = $m; $best = @($a, $b) }
      }
    }
    if ($best) { $result = $best }
  }
  $g.Dispose(); $bmp.Dispose(); $f.Dispose(); $pfc.Dispose()
  return $result
}
function Get-TextWidth([string]$t, [string]$fontFile, [double]$size) {
  Add-Type -AssemblyName System.Drawing
  $pfc = New-Object System.Drawing.Text.PrivateFontCollection
  $pfc.AddFontFile($fontFile)
  $bmp = New-Object System.Drawing.Bitmap 10, 10
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $f = New-Object System.Drawing.Font($pfc.Families[0], [single]100, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
  $w = $g.MeasureString($t, $f, 20000, [System.Drawing.StringFormat]::GenericTypographic).Width * $size / 100.0
  $g.Dispose(); $bmp.Dispose(); $f.Dispose(); $pfc.Dispose()
  return $w
}
function Get-InkBox([string]$png, [int]$y0, [int]$y1) {
  Add-Type -AssemblyName System.Drawing
  $bmp = [System.Drawing.Bitmap]::FromFile($png)
  $minx = 99999; $maxx = -1; $miny = 99999; $maxy = -1
  for ($y = [math]::Max(0, $y0); $y -lt [math]::Min($bmp.Height, $y1); $y++) {
    for ($x = 0; $x -lt $bmp.Width; $x += 2) {
      if ($bmp.GetPixel($x, $y).A -gt 128) {
        if ($x -lt $minx) { $minx = $x }; if ($x -gt $maxx) { $maxx = $x }
        if ($y -lt $miny) { $miny = $y }; if ($y -gt $maxy) { $maxy = $y }
      }
    }
  }
  $w = $bmp.Width; $h = $bmp.Height
  $bmp.Dispose()
  return [pscustomobject]@{ X0 = $minx; X1 = $maxx; Y0 = $miny; Y1 = $maxy; W = $w; H = $h }
}

# ================================================================== PRINCIPAL
$script:BoundCli = $PSBoundParameters
$exitCode = 0
$runDir = $null
try {
  Say ''
  Say '=== Prémontage — vérifications ==='
  # ---- outils
  $script:ffmpeg = (Get-Command ffmpeg -ErrorAction SilentlyContinue).Source
  $script:ffprobe = (Get-Command ffprobe -ErrorAction SilentlyContinue).Source
  if (-not $script:ffmpeg -or -not $script:ffprobe) { throw "ffmpeg et ffprobe sont introuvables dans le PATH. Rien n'a été installé." }
  $verLine = (Invoke-Tool $script:ffmpeg @('-hide_banner', '-version') '' -NoLog).Out.Split("`n")[0].Trim()
  Add-Check 'OK' "Outils trouvés : $verLine"

  # ---- entrees
  foreach ($pair in @(@('Rushes', $Rushes, 'dir'), @('Brief', $Brief, 'file'), @('Client', $Client, 'dir'))) {
    $ok = if ($pair[2] -eq 'dir') { Test-Path -LiteralPath $pair[1] -PathType Container } else { Test-Path -LiteralPath $pair[1] -PathType Leaf }
    if (-not $ok) { throw ("Entrée introuvable : -{0} = {1}" -f $pair[0], $pair[1]) }
  }
  if ($Musique -and -not (Test-Path -LiteralPath $Musique -PathType Leaf)) { throw "Musique introuvable : $Musique" }
  if ($Plan -and -not (Test-Path -LiteralPath $Plan -PathType Leaf)) { throw "Plan introuvable : $Plan" }
  if ($Transcription -and -not (Test-Path -LiteralPath $Transcription -PathType Leaf)) { throw "Transcription introuvable : $Transcription" }
  $Rushes = (Resolve-Path -LiteralPath $Rushes).Path
  $Brief = (Resolve-Path -LiteralPath $Brief).Path
  $Client = (Resolve-Path -LiteralPath $Client).Path
  if ($Musique) { $Musique = (Resolve-Path -LiteralPath $Musique).Path }
  if ($Plan) { $Plan = (Resolve-Path -LiteralPath $Plan).Path }
  # Le dossier de sortie est vérifié AVANT d'être créé : jamais dans le dossier des rushes.
  $Sortie = [IO.Path]::GetFullPath($(if ([IO.Path]::IsPathRooted($Sortie)) { $Sortie } else { Join-Path (Get-Location).Path $Sortie }))
  if ((($Sortie.TrimEnd('\') + '\').ToLowerInvariant()).StartsWith(($Rushes.TrimEnd('\') + '\').ToLowerInvariant())) { throw "Le dossier de sortie ne doit pas se trouver dans le dossier des rushes : les originaux ne sont jamais touchés." }
  if (-not (Test-Path -LiteralPath $Sortie)) { New-Item -ItemType Directory -Force -Path $Sortie | Out-Null }
  Add-Check 'OK' "Entrées trouvées (rushes, brief, dossier client$(if($Musique){', musique'})$(if($Plan){', plan'}))."

  # ---- parametres client
  $script:cfg = $null
  $cfgPath = Join-Path $Client 'parametres-script.json'
  if (Test-Path -LiteralPath $cfgPath) {
    $script:cfg = [IO.File]::ReadAllText($cfgPath, $utf8) | ConvertFrom-Json
    Add-Check 'OK' ("Paramètres client lus : {0}" -f $script:cfg.marque)
  }
  else { Add-Check 'ATTENTION' "Pas de parametres-script.json dans le dossier client : valeurs par défaut du script."; $script:warnings.Add('Pas de paramètres client.') }

  # ---- brief
  $briefText = [IO.File]::ReadAllText($Brief, $utf8)
  $titre = ''
  if ($briefText -match '(?m)Titre de la vid[ée]o\s*:\s*(.+)$') { $titre = $Matches[1].Trim() }
  if (-not $titre) { $titre = Split-Path $Rushes -Leaf }
  $aCompleter = ([regex]::Matches($briefText, 'À compléter')).Count
  Add-Check 'OK' ("Brief lu : titre « {0} » ; {1} mention(s) « À compléter » restante(s) (le script ne comprend pas le brief en profondeur)." -f $titre, $aCompleter)

  # ---- dossier de sortie (toujours nouveau)
  $stamp = Get-Date -Format 'yyyy-MM-dd_HHmmss'
  $runDir = Join-Path $Sortie ("{0}_{1}" -f $stamp, (Get-Slug $titre))
  $segDir = Join-Path $runDir 'segments'; $preDir = Join-Path $runDir 'premontage'
  $txtDir = Join-Path $runDir 'texte'; $ctrDir = Join-Path $runDir 'controle'
  $script:tmp = Join-Path $ctrDir '_tmp'
  foreach ($d in $segDir, $preDir, $ctrDir, $script:tmp) { New-Item -ItemType Directory -Force -Path $d | Out-Null }
  Copy-Item -LiteralPath $Brief -Destination (Join-Path $ctrDir 'brief-utilise.md')
  if (Test-Path -LiteralPath $cfgPath) { Copy-Item -LiteralPath $cfgPath -Destination (Join-Path $ctrDir 'parametres-client-utilises.json') }
  if ($Plan) { Copy-Item -LiteralPath $Plan -Destination (Join-Path $ctrDir 'plan-fourni.csv') }
  Say ("Nouveau dossier de sortie : {0}" -f $runDir)

  # ---- parametres effectifs
  $W = [int](Resolve-Param 'largeur de sortie (px)' $null $null 'largeur' 1080)
  $H = [int](Resolve-Param 'hauteur de sortie (px)' $null $null 'hauteur' 1920)
  $dureePlanEff = [double](Resolve-Param 'durée par plan pour la proposition (s)' 'DureePlan' $(if ($DureePlan -gt 0) { $DureePlan } else { $null }) 'duree_plan_proposition' 2.0)
  $dureeCibleEff = [string](Resolve-Param 'durée cible totale (s)' 'DureeCible' $(if ($DureeCible) { $DureeCible } else { $null }) 'duree_cible' '')
  $script:paramRows.Add([pscustomobject]@{ Nom = 'orientation'; Valeur = $(if ($OrientationParRush) { "$Orientation ; par rush : $OrientationParRush" } else { $Orientation }); Source = $(if ($PSBoundParameters.ContainsKey('Orientation')) { 'ligne de commande' } else { 'défaut du script' }); Statut = 'choix de cet essai (propre à ces fichiers)' })
  $script:paramRows.Add([pscustomobject]@{ Nom = 'son d''origine'; Valeur = $SonOrigine; Source = $(if ($PSBoundParameters.ContainsKey('SonOrigine')) { 'ligne de commande' } else { 'défaut du script (prudent : le son n''est pas écouté)' }); Statut = 'choix de cet essai' })

  # ---- inventaire des rushes
  $exts = '.mov', '.mp4', '.m4v', '.mkv', '.avi', '.mts', '.mxf'
  $files = @(Get-ChildItem -LiteralPath $Rushes -File | Where-Object { $exts -contains $_.Extension.ToLowerInvariant() } | Sort-Object Name)
  if ($files.Count -eq 0) { throw "Aucun fichier vidéo trouvé dans $Rushes" }
  $before = $files | ForEach-Object { "{0}|{1}|{2}" -f $_.Name, $_.Length, $_.LastWriteTimeUtc.Ticks }
  $info = @{}
  $invalid = @()
  foreach ($f in $files) {
    $pr = Get-Probe $f.FullName
    $v = $null; if ($pr) { $v = $pr.streams | Where-Object { $_.codec_type -eq 'video' } | Select-Object -First 1 }
    $dur = 0.0; if ($pr -and $pr.format.duration) { $dur = [double]::Parse($pr.format.duration, $ci) }
    if (-not $v -or $dur -le 0) { $invalid += $f.Name; continue }
    $rot = 0
    $sd = $v.PSObject.Properties['side_data_list']
    if ($sd) { $r = $v.side_data_list | Where-Object { $_.PSObject.Properties.Name -contains 'rotation' } | Select-Object -First 1; if ($r) { $rot = [int]$r.rotation } }
    if ($rot -eq 0 -and $v.PSObject.Properties['tags'] -and $v.tags.PSObject.Properties['rotate']) { $rot = [int]$v.tags.rotate }
    $ew = [int]$v.width; $eh = [int]$v.height
    if ([math]::Abs($rot) -eq 90 -or [math]::Abs($rot) -eq 270) { $t0 = $ew; $ew = $eh; $eh = $t0 }
    $range = ''; if ($v.PSObject.Properties['color_range']) { $range = [string]$v.color_range }
    $cs = ''; if ($v.PSObject.Properties['color_space']) { $cs = [string]$v.color_space }
    $hasAudio = [bool]($pr.streams | Where-Object { $_.codec_type -eq 'audio' })
    $info[$f.Name] = [pscustomobject]@{
      Fichier = $f; Nom = $f.Name; Base = $f.BaseName; Dur = $dur; W = [int]$v.width; H = [int]$v.height; EW = $ew; EH = $eh; Rot = $rot
      Fps = Parse-Fps ([string]$v.r_frame_rate); FpsTxt = [string]$v.r_frame_rate; Codec = [string]$v.codec_name; Pix = [string]$v.pix_fmt
      Full = ($range -eq 'pc' -or ([string]$v.pix_fmt) -like 'yuvj*'); Bt709 = ($cs -eq 'bt709'); Audio = $hasAudio
    }
  }
  $files = @($files | Where-Object { $info.ContainsKey($_.Name) })
  if ($invalid.Count -gt 0) { Add-Check 'ATTENTION' ("Fichiers ignorés (illisibles ou sans image) : {0}" -f ($invalid -join ', ')); $script:warnings.Add('Fichiers ignorés : ' + ($invalid -join ', ')) }
  if ($files.Count -eq 0) { throw 'Aucun rush lisible.' }
  $totalSrc = ($files | ForEach-Object { $info[$_.Name].Dur } | Measure-Object -Sum).Sum
  Add-Check 'OK' ("{0} rush(es) lisible(s), durée totale {1} s." -f $files.Count, (Fmt $totalSrc))
  $fpsTxt = $info[$files[0].Name].FpsTxt
  if ($fpsTxt -notmatch '^\d+/\d+$' -or (Parse-Fps $fpsTxt) -le 0) { $fpsTxt = '30' }
  $script:paramRows.Add([pscustomobject]@{ Nom = 'images par seconde de sortie'; Valeur = $fpsTxt; Source = 'fréquence du premier rush'; Statut = 'technique' })

  # ---- orientation
  $prefix = @{}
  $needDecision = @()
  $orientUsed = @{}
  # Orientation décidée rush par rush (-OrientationParRush "DGM_3828=anti-horaire;DGM_3832=horaire") : prioritaire sur -Orientation.
  $orMap = @{}
  if ($OrientationParRush) {
    foreach ($pair in ($OrientationParRush -split '[;,]')) {
      if (-not $pair.Trim()) { continue }
      if ($pair -match '^\s*([^=]+?)\s*=\s*(\S+)\s*$') {
        $ovKey = [IO.Path]::GetFileNameWithoutExtension($Matches[1].Trim()).ToLowerInvariant(); $ovVal = $Matches[2]
        if (@('aucune', 'anti-horaire', 'horaire', 'recadrer-centre') -notcontains $ovVal) { throw "-OrientationParRush : valeur inconnue « $ovVal » (attendu : aucune, anti-horaire, horaire, recadrer-centre)." }
        if (-not ($files | Where-Object { $_.BaseName.ToLowerInvariant() -eq $ovKey })) { $script:warnings.Add("-OrientationParRush : aucun rush nommé « $ovKey » dans le dossier.") }
        $orMap[$ovKey] = $ovVal
      }
      else { throw "-OrientationParRush : entrée illisible « $pair » (attendu : NOM=valeur)." }
    }
  }
  foreach ($f in $files) {
    $i = $info[$f.Name]
    $targetPortrait = ($H -gt $W)
    $srcLandscape = ($i.EW -gt $i.EH)
    if ($i.Rot -ne 0) { $prefix[$f.Name] = ''; continue }                      # le fichier porte une indication de rotation : ffmpeg l'applique
    $oEff = $Orientation
    if ($orMap.ContainsKey($i.Base.ToLowerInvariant())) { $oEff = $orMap[$i.Base.ToLowerInvariant()] }
    if ($targetPortrait -and $srcLandscape) {
      $orientUsed[$f.Name] = $oEff
      switch ($oEff) {
        'anti-horaire' { $prefix[$f.Name] = 'transpose=2,' }
        'horaire' { $prefix[$f.Name] = 'transpose=1,' }
        'recadrer-centre' { $prefix[$f.Name] = ('crop=trunc(ih*{0}/{1}/2)*2:ih,' -f $W, $H) }
        'aucune' { $prefix[$f.Name] = '' }
        default { $needDecision += $f.Name; $prefix[$f.Name] = '' }
      }
    }
    else { $prefix[$f.Name] = '' }
  }
  if ($needDecision.Count -gt 0) {
    Say ''
    Say '=== Orientation à décider par une personne ==='
    Add-Check 'ARRET' ("{0} rush(es) sont en format paysage sans indication de rotation, alors que la sortie est verticale. Le script ne peut pas deviner le sens." -f $needDecision.Count)
    foreach ($nd in $needDecision) {
      $first = $info[$nd]
      $o1 = Join-Path $ctrDir ("orientation_{0}.png" -f $first.Base)
      [void](Invoke-Ffmpeg @('-ss', (Fmt ($first.Dur / 2)), '-i', $first.Fichier.FullName, '-frames:v', '1', '-filter_complex', 'split=3[a][b][c];[a]scale=-1:640[o];[b]transpose=1,scale=-1:640[h];[c]transpose=2,scale=-1:640[ah];[o][h][ah]hstack=inputs=3', $o1) 'image de test d''orientation')
      Say ("  Image de test pour {0} : {1}" -f $first.Nom, $o1)
    }
    Say '  De gauche à droite : image d''origine | rotation HORAIRE | rotation ANTI-HORAIRE. Repérez celle où le décor est à l''endroit.'
    Say '  Relancez avec : -Orientation horaire  ou  -Orientation anti-horaire  (ou  recadrer-centre  si les rushes sont réellement paysage).'
    Say '  Si les rushes diffèrent, décidez chacun : -OrientationParRush "DGM_0001=horaire;DGM_0002=anti-horaire".'
    Add-Todo "Regarder l'image de test d'orientation et choisir la rotation (-Orientation)."
    $exitCode = 3
    throw [System.OperationCanceledException]::new('orientation')
  }
  foreach ($f in $files) {
    $i = $info[$f.Name]
    if ($i.Rot -ne 0) { Add-Check 'OK' ("{0} : rotation {1}° lue dans le fichier, appliquée automatiquement." -f $f.Name, $i.Rot) }
  }
  $appliedOrient = ($files | ForEach-Object { $prefix[$_.Name] } | Where-Object { $_ } | Select-Object -Unique)
  if ($appliedOrient) {
    $usedTxt = (($files | Where-Object { $orientUsed.ContainsKey($_.Name) } | ForEach-Object { "{0}={1}" -f $_.BaseName, $orientUsed[$_.Name] }) -join ', ')
    Add-Check 'OK' ("Orientation appliquée rush par rush ({0}) : décidée hors du script (-Orientation ou -OrientationParRush, après regard d'une image de test), jamais déduite par le script." -f $usedTxt)
    Add-Todo "Confirmer sur les planches de contrôle (controle\planche-rushes-*.png) que les rushes sont à l'endroit." }

  # ---- planches des rushes
  $fontArial = Esc-FilterPath 'C:\Windows\Fonts\arial.ttf'
  $rowFiles = @()
  foreach ($f in $files) {
    $i = $info[$f.Name]
    $row = Join-Path $script:tmp ("row_{0}.png" -f (Esc-Label $i.Base))
    $vf = "{0}fps=5/{1},scale=216:384:force_original_aspect_ratio=decrease,pad=216:384:(ow-iw)/2:(oh-ih)/2,drawtext=fontfile='{2}':text='{3}':x=6:y=6:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6,tile=5x1" -f $prefix[$f.Name], (Fmt $i.Dur), $fontArial, (Esc-Label $i.Base)
    [void](Invoke-Ffmpeg @('-i', $f.FullName, '-vf', $vf, '-frames:v', '1', $row) ("planche {0}" -f $f.Name))
    $rowFiles += $row
  }
  $sheetIdx = 0
  for ($k = 0; $k -lt $rowFiles.Count; $k += 6) {
    $grp = @($rowFiles[$k..([math]::Min($k + 5, $rowFiles.Count - 1))])
    $sheetIdx++
    $out = Join-Path $ctrDir ("planche-rushes-{0}.png" -f $sheetIdx)
    if ($grp.Count -eq 1) { Copy-Item -LiteralPath $grp[0] -Destination $out -Force }
    else {
      $a = @(); foreach ($g in $grp) { $a += '-i'; $a += $g }
      [void](Invoke-Ffmpeg ($a + @('-filter_complex', ("vstack=inputs={0}" -f $grp.Count), $out)) 'planche des rushes')
    }
  }
  Add-Check 'OK' ("{0} planche(s) de contrôle des rushes créée(s) dans controle\ (5 images par rush, orientation appliquée)." -f $sheetIdx)

  # ---- plan
  $planRows = @()
  if ($Plan) {
    $csv = Import-Csv -LiteralPath $Plan -Delimiter ';' -Encoding UTF8
    foreach ($r in ($csv | Sort-Object { [int]$_.ordre })) {
      $match = $files | Where-Object { $_.BaseName -ieq $r.rush -or $_.Name -ieq $r.rush } | Select-Object -First 1
      if (-not $match) { throw ("Plan : rush introuvable « {0} » (ligne ordre {1})." -f $r.rush, $r.ordre) }
      $deb = [double]::Parse(([string]$r.debut).Replace(',', '.'), $ci); $du = [double]::Parse(([string]$r.duree).Replace(',', '.'), $ci)
      $d = $info[$match.Name].Dur
      if ($deb -lt 0 -or $du -le 0 -or ($deb + $du) -gt ($d + 0.05)) { throw ("Plan : extrait hors du rush {0} (début {1} + durée {2} > {3} s)." -f $match.Name, $deb, $du, (Fmt $d)) }
      $planRows += [pscustomobject]@{ Ordre = [int]$r.ordre; Rush = $match.Name; Debut = $deb; Duree = $du; Nom = [string]$r.nom; Note = [string]$r.note }
    }
    Add-Check 'OK' ("Plan fourni lu : {0} plan(s). Sélection, ordre et durées décidés par une personne (pas par le script)." -f $planRows.Count)
  }
  else {
    Say ''
    Say '=== Proposition technique de plan (aucun plan fourni) ==='
    $ordre = 0
    $blurs = @{}
    foreach ($f in $files) {
      $i = $info[$f.Name]
      $bf = Join-Path $script:tmp 'bl.txt'; if (Test-Path -LiteralPath $bf) { Remove-Item -LiteralPath $bf -Force }
      [void](Invoke-Ffmpeg @('-i', $f.FullName, '-vf', 'fps=5,scale=480:-2,blurdetect,metadata=print:file=bl.txt', '-an', '-f', 'null', 'NUL') ("netteté {0}" -f $f.Name) $script:tmp)
      $vals = @(); if (Test-Path -LiteralPath $bf) { foreach ($l in [IO.File]::ReadLines($bf)) { $m = [regex]::Match($l, 'lavfi\.blur=([\d.]+)'); if ($m.Success) { $vals += [double]::Parse($m.Groups[1].Value, $ci) } } }
      $blurs[$f.Name] = $vals
    }
    $allMeans = @($files | ForEach-Object { $v = $blurs[$_.Name]; if ($v.Count) { ($v | Measure-Object -Average).Average } })
    $sortedMeans = $allMeans | Sort-Object
    $medBlur = if ($sortedMeans.Count) { $sortedMeans[[int][math]::Floor($sortedMeans.Count / 2)] } else { 0 }
    foreach ($f in $files) {
      $i = $info[$f.Name]
      $du = [math]::Min($dureePlanEff, $i.Dur)
      $vals = $blurs[$f.Name]
      $margin = 0.2
      $startMax = $i.Dur - $margin - $du
      $deb = [math]::Max(0.0, ($i.Dur - $du) / 2)
      if ($vals.Count -ge 3 -and $startMax -ge $margin) {
        $nWin = [math]::Max(1, [int][math]::Round($du * 5)); $bestScore = [double]::MaxValue
        for ($s = $margin; $s -le $startMax + 0.001; $s += 0.2) {
          $a = [int][math]::Round($s * 5); $b = [math]::Min($vals.Count, $a + $nWin)
          if ($b -le $a) { continue }
          $sc = ($vals[$a..($b - 1)] | Measure-Object -Average).Average
          if ($sc -lt $bestScore) { $bestScore = $sc; $deb = $s }
        }
      }
      $mean = if ($vals.Count) { ($vals | Measure-Object -Average).Average } else { 0 }
      $note = 'proposition technique (netteté)'
      if ($medBlur -gt 0 -and $mean -gt ($medBlur * 1.25)) { $note += ' - plus flou que la médiane : à examiner' }
      if ($i.Dur -lt ($dureePlanEff + 0.4)) { $note += ' - rush court' }
      $ordre++
      $planRows += [pscustomobject]@{ Ordre = $ordre; Rush = $f.Name; Debut = [math]::Round($deb, 2); Duree = [math]::Round($du, 2); Nom = (Get-Slug $i.Base); Note = $note }
    }
    $propLines = @('ordre;rush;debut;duree;nom;note')
    foreach ($r in $planRows) { $propLines += ("{0:00};{1};{2};{3};{4};{5}" -f $r.Ordre, $r.Rush.Substring(0, $r.Rush.Length - [IO.Path]::GetExtension($r.Rush).Length), (Fmt $r.Debut), (Fmt $r.Duree), $r.Nom, $r.Note) }
    $propPath = Join-Path $ctrDir 'plan-propose.csv'
    [IO.File]::WriteAllText($propPath, (($propLines -join "`r`n") + "`r`n"), $utf8)
    Add-Check 'OK' ("Proposition technique écrite : {0} (chaque rush, ordre des noms de fichiers, extrait le plus net de {1} s)." -f $propPath, (Fmt $dureePlanEff))
    Add-Todo 'Le plan proposé est seulement technique (netteté, ordre des noms de fichiers). Une personne doit choisir les plans, l''ordre et les durées (pertinence, promotions, personnes, marques, rythme).'
    if (-not $Auto) {
      Say ''
      Say '=== Arrêt volontaire : plan à valider ==='
      Say ("  Regardez les planches de contrôle (controle\planche-rushes-*.png) et le fichier {0}." -f $propPath)
      Say '  Corrigez-le (retirer, réordonner, ajuster début et durée), puis relancez avec : -Plan <ce fichier>'
      Say '  (ou ajoutez -Auto pour produire quand même à partir de la proposition : sortie marquée NON VALIDÉE).'
      $exitCode = 0
      throw [System.OperationCanceledException]::new('plan')
    }
    Add-Todo 'SORTIE NON VALIDÉE : produite avec -Auto à partir de la proposition technique, sans choix humain des plans.'
  }
  $planRows = @($planRows | Sort-Object Ordre)
  $totalDur = ($planRows | Measure-Object -Property Duree -Sum).Sum
  if ($dureeCibleEff -match '^\s*(\d+(?:[.,]\d+)?)\s*-\s*(\d+(?:[.,]\d+)?)\s*$') {
    $mn = [double]::Parse($Matches[1].Replace(',', '.'), $ci); $mx = [double]::Parse($Matches[2].Replace(',', '.'), $ci)
    if ($totalDur -lt $mn -or $totalDur -gt $mx) { Add-Check 'ATTENTION' ("Durée totale {0} s hors de la cible {1}-{2} s." -f (Fmt $totalDur), $mn, $mx); $script:warnings.Add('Durée hors cible.') }
    else { Add-Check 'OK' ("Durée totale {0} s dans la cible {1}-{2} s." -f (Fmt $totalDur), $mn, $mx) }
  }
  [IO.File]::WriteAllText((Join-Path $ctrDir 'plan-utilise.csv'), ((@('ordre;rush;debut;duree;nom;note') + ($planRows | ForEach-Object { "{0:00};{1};{2};{3};{4};{5}" -f $_.Ordre, $_.Rush, (Fmt $_.Debut), (Fmt $_.Duree), $_.Nom, $_.Note })) -join "`r`n") + "`r`n", $utf8)

  # ================================================================== PRODUCTION
  Say ''
  Say '=== Production ==='
  # ---- segments
  $segFiles = @()
  $n = $planRows.Count
  foreach ($r in $planRows) {
    $i = $info[$r.Rush]
    $sc = "scale={0}:{1}:flags=lanczos" -f $W, $H
    if ($i.EH -gt 0 -and $prefix[$r.Rush] -eq '' -and ([math]::Abs(($i.EW / $i.EH) - ($W / $H)) -gt 0.02)) {
      $sc = "scale={0}:{1}:force_original_aspect_ratio=decrease:flags=lanczos,pad={0}:{1}:(ow-iw)/2:(oh-ih)/2" -f $W, $H
      $script:warnings.Add("$($r.Rush) : proportions différentes de la sortie, bandes noires ajoutées.")
    }
    if ($i.Full) { $sc += ':in_range=full:out_range=tv' }
    $vf = "{0}{1},fps={2},format=yuv420p,setsar=1" -f $prefix[$r.Rush], $sc, $fpsTxt
    $o = Join-Path $segDir ("{0:00}_{1}_{2}.mp4" -f $r.Ordre, $i.Base, $(if ($r.Nom) { Get-Slug $r.Nom } else { 'plan' }))
    $a = @('-ss', (Fmt $r.Debut), '-i', $i.Fichier.FullName, '-t', (Fmt $r.Duree), '-vf', $vf, '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-pix_fmt', 'yuv420p')
    if ($i.Bt709) { $a += @('-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709') }
    if ($i.Audio) { $a += @('-c:a', 'aac', '-b:a', '256k', '-ar', '48000') } else { $a += '-an' }
    $a += @('-movflags', '+faststart', $o)
    [void](Invoke-Ffmpeg $a ("segment {0}" -f $r.Ordre))
    $segFiles += $o
  }
  Add-Check 'OK' ("{0} segment(s) exporté(s) dans segments\ ({1}x{2}, {3} i/s, H.264, son d'origine conservé quand il existe)." -f $segFiles.Count, $W, $H, $fpsTxt)
  $anyNoBt = @($files | Where-Object { -not $info[$_.Name].Bt709 })
  if ($anyNoBt.Count -gt 0) { $script:warnings.Add('Au moins un rush n''est pas marqué BT.709 : pas de marquage colorimétrique, vérifier les couleurs.'); Add-Todo 'Vérifier les couleurs (rush non BT.709).' }

  # ---- musique
  $music = $null
  if ($Musique) {
    Say ''
    Say '--- Analyse de la musique ---'
    $mp = Get-Probe $Musique
    $mdur = [double]::Parse($mp.format.duration, $ci)
    $cuts = @(); $acc = 0.0; foreach ($r in $planRows) { $acc += $r.Duree; if ($r -ne $planRows[-1]) { $cuts += [math]::Round($acc, 2) } }
    $an = Get-MusicAnalysis $Musique $totalDur $cuts 60.0 $DepartMusique
    if ($an.PSObject.Properties['FenetreOK'] -and -not $an.FenetreOK) { $script:warnings.Add('La fenêtre musicale imposée contient un quasi-silence : vérifier à l''écoute.') }
    $dep = $an.Depart; $depSrc = 'analyse du début de la piste'
    if ($DepartMusique -ge 0) { $dep = $DepartMusique; $depSrc = 'imposé par -DepartMusique' }
    $fin = $an.FonduEntree; $finSrc = 'ajusté à l''extrait (analyse)'
    if ($FonduEntree -ge 0) { $fin = $FonduEntree; $finSrc = 'imposé' }
    $fout = $an.FonduSortie; $foutSrc = 'ajusté à l''extrait (analyse)'
    if ($FonduSortie -ge 0) { $fout = $FonduSortie; $foutSrc = 'imposé' }
    if (($dep + $totalDur) -gt ($mdur + 0.05)) { throw ("La piste ({0} s) est trop courte pour un départ à {1} s et une vidéo de {2} s." -f (Fmt $mdur), (Fmt $dep), (Fmt $totalDur)) }
    $script:paramRows.Add([pscustomobject]@{ Nom = 'départ de la musique (s)'; Valeur = (Fmt $dep); Source = $depSrc; Statut = 'choix propre à ce fichier : ne pas réutiliser pour une autre piste' })
    $script:paramRows.Add([pscustomobject]@{ Nom = 'fondu d''entrée (s)'; Valeur = (Fmt $fin); Source = $finSrc; Statut = 'choix propre à cet extrait' })
    $script:paramRows.Add([pscustomobject]@{ Nom = 'fondu de sortie (s)'; Valeur = (Fmt $fout); Source = $foutSrc; Statut = 'choix propre à cet extrait' })
    $script:paramRows.Add([pscustomobject]@{ Nom = 'gain de la musique (dB)'; Valeur = (Fmt $GainMusiqueDb); Source = $(if ($PSBoundParameters.ContainsKey('GainMusiqueDb')) { 'ligne de commande' } else { 'défaut du script (aucun gain)' }); Statut = 'choix de cet essai' })
    $music = [pscustomobject]@{ Depart = $dep; In = $fin; Out = $fout; Analysis = $an }
    Say ("  Départ retenu : {0} s — {1}" -f (Fmt $dep), $an.Raison)
    Say ("  Fondu entrée {0} s, sortie {1} s ; niveau moyen des 1,5 dernières s : {2} dB (médiane de l'extrait : {3} dB)" -f (Fmt $fin), (Fmt $fout), $an.NiveauFin, $an.NiveauMedian)
    Say ("  Alignement attaques/coupes (indicatif) : {0}" -f $an.Alignement)
    if ($an.Alternatives.Count -gt 0) { Say ("  Autres départs possibles : {0} s" -f (($an.Alternatives | ForEach-Object { Fmt $_ }) -join ', ')) }
    Add-Todo "Écouter la musique avec la vidéo : le départ est choisi sur le signal, pas à l'oreille."
    Add-Todo "Confirmer le droit d'utiliser la piste (licence ou autorisation) et l'absence de paroles explicites : le script ne peut pas le vérifier."
    if ($mp.format.PSObject.Properties['tags']) { $tg = $mp.format.tags; $meta = @(); foreach ($k in 'title', 'artist', 'album') { if ($tg.PSObject.Properties[$k]) { $meta += "$k=$($tg.$k)" } }; if ($meta.Count) { Say ("  Étiquettes du fichier : {0}" -f ($meta -join ' ; ')) } else { Say '  Étiquettes du fichier : aucune (origine de la piste non identifiable).' } }
  }

  # ---- texte
  $textInfo = $null
  $cntInfo = @()
  if ($Compteur -and -not $Texte) { throw '-Compteur demande aussi -Texte (le compteur reprend la police, la taille et le style du texte).' }
  if ($Texte) {
    Say ''
    Say '--- Texte ---'
    New-Item -ItemType Directory -Force -Path $txtDir | Out-Null
    if ($PoliceTexte -and -not (Test-Path -LiteralPath $PoliceTexte -PathType Leaf)) { throw "Police du texte introuvable : $PoliceTexte" }
    $fontFile = [string](Resolve-Param 'fichier de police du texte' 'PoliceTexte' $(if ($PoliceTexte) { (Resolve-Path -LiteralPath $PoliceTexte).Path } else { $null }) 'police_texte_fichier' '')
    if (-not $fontFile -or -not (Test-Path -LiteralPath $fontFile)) {
      foreach ($c in (Join-Path $env:LOCALAPPDATA 'Microsoft\Windows\Fonts\Montserrat-Regular.ttf'), 'C:\Windows\Fonts\Montserrat-Regular.ttf') { if (Test-Path -LiteralPath $c) { $fontFile = $c; break } }
    }
    if (-not $fontFile -or -not (Test-Path -LiteralPath $fontFile)) { throw "Police du texte introuvable (paramètre police_texte_fichier du client). Le texte n'a pas été ajouté." }
    $size = [double](Resolve-Param 'taille du texte (px)' 'TexteTaille' $(if ($TexteTaille -gt 0) { $TexteTaille } else { $null }) 'texte_taille' 52)
    $color = ([string](Resolve-Param 'couleur du texte (HEX)' $null $null 'texte_couleur' 'FFFFFF')).TrimStart('#')
    $mb = [double](Resolve-Param 'marge basse du texte (px)' $null $null 'texte_marge_basse' 458)
    $ml = [double](Resolve-Param 'marge latérale du texte (px)' $null $null 'texte_marge_laterale' 130)
    $op = [double](Resolve-Param 'opacité de l''ombre' $null $null 'texte_ombre_opacite' 0.7)
    $sg = [double](Resolve-Param 'flou de l''ombre (px)' 'TexteOmbreFlou' $(if ($TexteOmbreFlou -ge 0) { $TexteOmbreFlou } else { $null }) 'texte_ombre_flou' 6)
    $sdy = [double](Resolve-Param 'décalage vertical de l''ombre (px)' 'TexteOmbreDecalage' $(if ($TexteOmbreDecalage -ge 0) { $TexteOmbreDecalage } else { $null }) 'texte_ombre_decalage' 3)
    $leadF = [double](Resolve-Param 'interligne du texte (multiple de la taille)' 'TexteInterligne' $(if ($TexteInterligne -gt 0) { $TexteInterligne } else { $null }) 'texte_interligne' 1.27)
    $cyFrac = -1.0
    if ($TexteCentreY -ge 0) { $cyFrac = $TexteCentreY; $script:paramRows.Add([pscustomobject]@{ Nom = 'position verticale du centre du texte (fraction de la hauteur)'; Valeur = (Fmt $cyFrac); Source = 'ligne de commande'; Statut = 'choix de cet essai (remplace la marge basse)' }) }
    $lines = @(Get-TextLines $Texte $fontFile $size ($W - 2 * $ml))
    while ($true) {
      $widest = ($lines | ForEach-Object { Get-TextWidth $_ $fontFile $size } | Measure-Object -Maximum).Maximum
      if ($widest -le ($W - 2 * $ml) -or $size -le 36) { break }
      $size -= 2
      $script:warnings.Add("Texte trop large : taille réduite à $size px.")
    }
    if ($widest -gt ($W - 2 * $ml)) { $script:warnings.Add('Texte plus large que les marges latérales même à la taille minimale (36 px).') }
    $lead = [math]::Round($size * $leadF)
    if ($cyFrac -ge 0) { $yFirst = [math]::Round($H * $cyFrac - ($lines.Count * $lead) / 2) }
    else {
      $yLast = [math]::Round($H - $mb - 0.98 * $size)
      $yFirst = $yLast - ($lines.Count - 1) * $lead
    }
    $tech = Join-Path $txtDir '_technique'; New-Item -ItemType Directory -Force -Path $tech | Out-Null
    $fp = Esc-FilterPath $fontFile
    $ovPng = Join-Path $txtDir 'texte_overlay.png'
    for ($k = 0; $k -lt $lines.Count; $k++) { [IO.File]::WriteAllText((Join-Path $tech ("ligne{0}.txt" -f ($k + 1))), $lines[$k], $utf8) }
    # Avec -TexteCentreY : deux passes (rendu, mesure de l'encre, recentrage), quelle que soit la police.
    $passes = $(if ($cyFrac -ge 0) { 2 } else { 1 })
    $ink = $null
    for ($pass = 1; $pass -le $passes; $pass++) {
      $dt = @(); for ($k = 0; $k -lt $lines.Count; $k++) {
        $dt += ("drawtext=fontfile='{0}':textfile='ligne{1}.txt':fontsize={2}:fontcolor=0x{3}:x=(w-text_w)/2:y={4}" -f $fp, ($k + 1), (Fmt $size), $color, ($yFirst + $k * $lead))
      }
      $fc = ("color=c=black@0.0:s={0}x{1}:r=1,format=rgba," -f $W, $H) + ($dt -join ',') + "[txt];[txt]split[a][b];[a]colorchannelmixer=rr=0:gg=0:bb=0:aa=$(Fmt $op),gblur=sigma=$(Fmt $sg)[sh];[sh][b]overlay=x=0:y=$(Fmt $sdy):format=auto,format=rgba"
      [IO.File]::WriteAllText((Join-Path $tech 'filtre-overlay.txt'), $fc, $utf8)
      [void](Invoke-Ffmpeg @('-filter_complex_script', 'filtre-overlay.txt', '-frames:v', '1', $ovPng) 'image du texte' $tech)
      $ink = Get-InkBox $ovPng ([int]($yFirst - 40)) ([int]($yFirst + $lines.Count * $lead + $size + 40))
      if ($cyFrac -ge 0 -and $pass -eq 1 -and $ink.Y1 -ge 0) { $yFirst = $yFirst + [math]::Round($H * $cyFrac - ($ink.Y0 + $ink.Y1) / 2) }
    }
    [IO.File]::WriteAllText((Join-Path $txtDir 'texte.txt'), ($lines -join "`n"), $utf8)
    $ts = [TimeSpan]::FromSeconds($totalDur)
    $srtEnd = "{0:00}:{1:00}:{2:00},{3:000}" -f [int][math]::Floor($ts.TotalHours), $ts.Minutes, $ts.Seconds, $ts.Milliseconds
    [IO.File]::WriteAllText((Join-Path $txtDir 'texte.srt'), ("1`n00:00:00,000 --> {0}`n{1}`n" -f $srtEnd, ($lines -join "`n")), $utf8)
    $textInfo =[pscustomobject]@{ Overlay = $ovPng; Lines = $lines; Size = $size; Ink = $ink; MargeBasse = ($H - $ink.Y1); MargeG = $ink.X0; MargeD = ($W - $ink.X1); Centre = (($ink.X0 + $ink.X1) / 2) }
    $tp = @("# Texte — paramètres utilisés", "", "Texte : « $($lines -join ' / ') »", "", "| Élément | Valeur |", "| --- | --- |",
      "| Police | $fontFile |", "| Taille | $(Fmt $size) px sur $W x $H |", "| Couleur | $color |", "| Boîte de fond | aucune (ombre douce : opacité $(Fmt $op), flou $(Fmt $sg) px, décalage $(Fmt $sdy) px) |",
      "| Alignement | centré horizontalement, $($lines.Count) ligne(s), interligne $(Fmt $lead) px ($(Fmt $leadF) x la taille) |",
      "| Position verticale | $(if ($cyFrac -ge 0) { 'centre du bloc à ' + (Fmt ($cyFrac * 100)) + ' % de la hauteur (position demandée)' } else { 'selon la marge basse demandée (' + (Fmt $mb) + ' px)' }) ; centre mesuré à $(Fmt ((($ink.Y0 + $ink.Y1) / 2) / $H * 100)) % |", "| Bloc mesuré | x $($ink.X0)-$($ink.X1), y $($ink.Y0)-$($ink.Y1) |",
      "| Marges mesurées | gauche $($textInfo.MargeG) px, droite $($textInfo.MargeD) px, bas $($textInfo.MargeBasse) px |", "",
      "Les marges viennent d'hypothèses de zones de sécurité (haut 250, bas 450, côtés 130 px) **non vérifiées dans les applications** : à tester sur téléphone.",
      '`texte.srt` est une légende d''habillage (une seule ligne de temps), pas une transcription.')
    [IO.File]::WriteAllText((Join-Path $txtDir 'texte_parametres.md'), ($tp -join "`r`n") + "`r`n", $utf8)
    Add-Check 'OK' ("Texte créé : {0} ligne(s), centre horizontal {1} px, marges G {2} / D {3} / bas {4} px." -f $lines.Count, $textInfo.Centre, $textInfo.MargeG, $textInfo.MargeD, $textInfo.MargeBasse)
    Add-Todo 'Regarder le texte sur toute la vidéo (lisibilité, éléments cachés) et le tester sur téléphone dans l''application de diffusion.'

    # ---- compteur facultatif : un chiffre par plan, même style que le texte (essai « réactions », 2026-11-24)
    $cntInfo = @()
    if ($Compteur) {
      $vals = @($Compteur -split '[;,]' | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne '' })
      if ($vals.Count -ne $planRows.Count) { throw ("-Compteur : {0} valeur(s) pour {1} plan(s) : il en faut une par plan." -f $vals.Count, $planRows.Count) }
      $acc = 0.0
      for ($k = 0; $k -lt $vals.Count; $k++) {
        [IO.File]::WriteAllText((Join-Path $tech ("compteur{0}.txt" -f ($k + 1))), $vals[$k], $utf8)
        $cpng = Join-Path $txtDir ("compteur_{0:00}.png" -f ($k + 1))
        $yy = [double]($H * $CompteurCentreY)
        $cink = $null
        for ($pass = 1; $pass -le 2; $pass++) {
          $dtc = ("drawtext=fontfile='{0}':textfile='compteur{1}.txt':fontsize={2}:fontcolor=0x{3}:x=(w-text_w)/2:y={4}" -f $fp, ($k + 1), (Fmt $size), $color, (Fmt $yy))
          $fcc = ("color=c=black@0.0:s={0}x{1}:r=1,format=rgba," -f $W, $H) + $dtc + "[txt];[txt]split[a][b];[a]colorchannelmixer=rr=0:gg=0:bb=0:aa=$(Fmt $op),gblur=sigma=$(Fmt $sg)[sh];[sh][b]overlay=x=0:y=$(Fmt $sdy):format=auto,format=rgba"
          [IO.File]::WriteAllText((Join-Path $tech 'filtre-compteur.txt'), $fcc, $utf8)
          [void](Invoke-Ffmpeg @('-filter_complex_script', 'filtre-compteur.txt', '-frames:v', '1', $cpng) ("image du compteur {0}" -f ($k + 1)) $tech)
          $cink = Get-InkBox $cpng ([int]($yy - 60)) ([int]($yy + $size + 60))
          if ($pass -eq 1 -and $cink.Y1 -ge 0) { $yy = $yy + [math]::Round($H * $CompteurCentreY - ($cink.Y0 + $cink.Y1) / 2) }
        }
        $d = $planRows[$k].Duree
        $cntInfo += [pscustomobject]@{ Valeur = $vals[$k]; Png = $cpng; Debut = $acc; Fin = ($acc + $d); Ink = $cink }
        $acc += $d
      }
      [IO.File]::WriteAllText((Join-Path $txtDir 'compteur.txt'), (($cntInfo | ForEach-Object { "{0};{1};{2}" -f $_.Valeur, (Fmt $_.Debut), (Fmt $_.Fin) }) -join "`r`n") + "`r`n", $utf8)
      Add-Check 'OK' ("Compteur créé : {0} valeur(s) ({1}), centre vertical mesuré à {2} % de la hauteur, même police et même taille que le texte." -f $cntInfo.Count, ($vals -join ', '), (Fmt ((($cntInfo[0].Ink.Y0 + $cntInfo[0].Ink.Y1) / 2) / $H * 100)))
    }
  }

  # ---- assemblage
  $inputs = @(); foreach ($s in $segFiles) { $inputs += '-i'; $inputs += $s }
  $lab = ''; for ($i = 0; $i -lt $n; $i++) { $lab += "[${i}:v]" }
  $venc = @('-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p')
  if (-not ($files | Where-Object { -not $info[$_.Name].Bt709 })) { $venc += @('-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709') }
  $aenc = @('-c:a', 'aac', '-b:a', '256k', '-ar', '48000')
  $audioMode = 'muet'
  $audioArgsIn = @(); $audioArgsOut = @('-an'); $graphAudio = ''; $mapA = @()
  if ($Musique) {
    $audioMode = 'musique'
    $audioArgsIn = @('-ss', (Fmt $music.Depart), '-t', (Fmt $totalDur), '-i', $Musique)
    $gain = ''; if ($GainMusiqueDb -ne 0) { $gain = ",volume=$(Fmt $GainMusiqueDb)dB" }
    $af = "afade=t=in:st=0:d=$(Fmt $music.In),afade=t=out:st=$(Fmt ($totalDur - $music.Out)):d=$(Fmt $music.Out)$gain"
    $audioArgsOut = @('-map', "$($n):a:0", '-af', $af) + $aenc
  }
  elseif ($SonOrigine -eq 'garder') {
    if (@($planRows | Where-Object { -not $info[$_.Rush].Audio }).Count -gt 0) { $script:warnings.Add("Un rush n'a pas de son : -SonOrigine garder ignoré (version muette)."); }
    else {
      $audioMode = 'audio-origine'
      $fa = ''; $labs = ''
      for ($i = 0; $i -lt $n; $i++) { $d = $planRows[$i].Duree; $fa += "[${i}:a]afade=t=in:st=0:d=0.04,afade=t=out:st=$(Fmt ($d - 0.04)):d=0.04[a$i];"; $labs += "[${i}:v][a$i]" }
      $graphAudio = $fa
    }
  }
  $variants = @(@{ Suffixe = ''; Texte = $false })
  if ($textInfo) { $variants = @(@{ Suffixe = '_sans-texte'; Texte = $false }, @{ Suffixe = '_avec-texte'; Texte = $true }) }
  $outFiles = @()
  foreach ($v in $variants) {
    $o = Join-Path $preDir ("premontage_{0}{1}.mp4" -f $audioMode, $v.Suffixe)
    $extraIn = @()
    $vchain = "${lab}concat=n=${n}:v=1:a=0[c]"
    if ($audioMode -eq 'audio-origine') { $vchain = $graphAudio + $labs + "concat=n=${n}:v=1:a=1[c][aud]" }
    if ($v.Texte) {
      $ovIdx = $n + $(if ($Musique) { 1 } else { 0 })
      $extraIn = @('-loop', '1', '-framerate', $fpsTxt, '-i', $textInfo.Overlay)
      $graph = $vchain + ";[${ovIdx}:v]format=rgba[ov];[c][ov]overlay=0:0:shortest=1,format=yuv420p[v]"
      if ($cntInfo -and $cntInfo.Count -gt 0) {
        $graph = $vchain + ";[${ovIdx}:v]format=rgba[ov];[c][ov]overlay=0:0:shortest=1[t0]"
        $prev = 't0'
        $fpsC = Parse-Fps $fpsTxt; if ($fpsC -le 0) { $fpsC = 30 }
        $fAcc = 0
        for ($k = 0; $k -lt $cntInfo.Count; $k++) {
          # bornes en NUMÉROS D'IMAGE (entiers) : un seul chiffre par image, changement exactement à la coupe
          $fN = [int][math]::Round($planRows[$k].Duree * $fpsC); $fA = $fAcc; $fB = $fAcc + $fN - 1; $fAcc += $fN
          $extraIn += @('-loop', '1', '-framerate', $fpsTxt, '-i', $cntInfo[$k].Png)
          $ci_ = $ovIdx + 1 + $k
          $last = ($k -eq $cntInfo.Count - 1)
          $outLab = $(if ($last) { 'tf' } else { "t$($k + 1)" })
          $graph += (";[${ci_}:v]format=rgba[cn$k];[$prev][cn$k]overlay=0:0:shortest=1:enable='between(n,{0},{1})'[{2}]" -f $fA, $fB, $outLab)
          $prev = $outLab
        }
        $graph += ";[tf]format=yuv420p[v]"
      }
    }
    else { $graph = $vchain + ";[c]format=yuv420p[v]" }
    $a = $inputs + $audioArgsIn + $extraIn + @('-filter_complex', $graph, '-map', '[v]')
    if ($audioMode -eq 'audio-origine') { $a += @('-map', '[aud]') + $aenc }
    else { $a += $audioArgsOut }
    $a += $venc + @('-movflags', '+faststart', '-t', (Fmt ($totalDur + 0.2)), $o)
    [void](Invoke-Ffmpeg $a ("prémontage {0}" -f (Split-Path $o -Leaf)))
    $outFiles += $o
  }
  Add-Check 'OK' ("Prémontage(s) exporté(s) : {0}" -f (($outFiles | ForEach-Object { Split-Path $_ -Leaf }) -join ', '))
  if ($audioMode -eq 'muet') { Add-Todo 'Version muette : ajouter une musique autorisée dans CapCut si souhaité.' }
  if ($audioMode -eq 'audio-origine') { Add-Todo "Écouter le son d'origine (voix, musique de la salle, paroles explicites) : non vérifiable par le script." }
  Add-Todo 'Regarder tous les plans : personnes identifiables sans autorisation confirmée, promotions ou offres, marques tierces, alcool mis en vedette. Le script ne peut pas les détecter.'

  # ---- controles techniques
  Say ''
  Say '--- Contrôles techniques ---'
  $fpsNum = Parse-Fps $fpsTxt; if ($fpsNum -le 0) { $fpsNum = 30 }
  foreach ($o in $outFiles) {
    $pr = Get-Probe $o
    $v = $pr.streams | Where-Object { $_.codec_type -eq 'video' } | Select-Object -First 1
    $au = $pr.streams | Where-Object { $_.codec_type -eq 'audio' } | Select-Object -First 1
    $d = [double]::Parse($pr.format.duration, $ci)
    $okDim = ([int]$v.width -eq $W -and [int]$v.height -eq $H)
    $okDur = ([math]::Abs($d - $totalDur) -le 0.15)
    $leaf = Split-Path $o -Leaf
    Add-Check $(if ($okDim) { 'OK' } else { 'ERREUR' }) ("{0} : {1}x{2} attendu {3}x{4}" -f $leaf, $v.width, $v.height, $W, $H)
    Add-Check $(if ($okDur) { 'OK' } else { 'ATTENTION' }) ("{0} : durée {1} s (plan : {2} s)" -f $leaf, (Fmt $d), (Fmt $totalDur))
    $cnt = (Invoke-Tool $script:ffprobe @('-v', 'error', '-select_streams', 'v:0', '-count_frames', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', $o) '' -NoLog).Out.Trim()
    $expected = [math]::Round($totalDur * $fpsNum)
    $okFr = ([math]::Abs([int]$cnt - $expected) -le $n + 2)
    Add-Check $(if ($okFr) { 'OK' } else { 'ATTENTION' }) ("{0} : {1} images (attendu environ {2})" -f $leaf, $cnt, $expected)
    $bf = Invoke-Tool $script:ffmpeg @('-hide_banner', '-i', $o, '-vf', 'blackdetect=d=0.1:pic_th=0.98,freezedetect=n=0.001:d=0.5', '-an', '-f', 'null', 'NUL') '' -NoLog
    $bad = @(($bf.Err -split "`n") | Where-Object { $_ -match 'black_start|freeze_start' })
    Add-Check $(if ($bad.Count -eq 0) { 'OK' } else { 'ATTENTION' }) ("{0} : images noires ou figées : {1}" -f $leaf, $(if ($bad.Count) { "$($bad.Count) détection(s)" } else { 'aucune détectée' }))
    if ($au) {
      $lf = Invoke-Tool $script:ffmpeg @('-hide_banner', '-i', $o, '-af', 'ebur128=peak=true', '-vn', '-f', 'null', 'NUL') '' -NoLog
      $mI = [regex]::Match($lf.Err, 'Integrated loudness:\s+I:\s+(-?[\d.]+) LUFS'); $mP = [regex]::Match($lf.Err, 'True peak:\s+Peak:\s+(-?[\d.]+) dBFS')
      $peak = if ($mP.Success) { [double]::Parse($mP.Groups[1].Value, $ci) } else { 0 }
      Add-Check $(if ($peak -gt -1.0) { 'ATTENTION' } else { 'OK' }) ("{0} : loudness {1} LUFS, pic réel {2} dBFS{3}" -f $leaf, $(if ($mI.Success) { $mI.Groups[1].Value } else { '?' }), $(if ($mP.Success) { $mP.Groups[1].Value } else { '?' }), $(if ($peak -gt -1.0) { ' (proche de l''écrêtage)' } else { '' }))
    }
    else { Add-Check 'OK' ("{0} : aucune piste audio (version muette)" -f $leaf) }
  }
  if ($textInfo) {
    Add-Check 'OK' ("Texte : centre horizontal à {0} px (idéal {1}), marges G {2} / D {3} / bas {4} px (hypothèses de zones de sécurité : haut 250, bas 450, côtés 130 px)." -f $textInfo.Centre, ($W / 2), $textInfo.MargeG, $textInfo.MargeD, $textInfo.MargeBasse)
    if ($textInfo.MargeBasse -lt 450 -or $textInfo.MargeG -lt 130 -or $textInfo.MargeD -lt 130) { Add-Check 'ATTENTION' 'Une marge du texte est inférieure aux hypothèses de zone de sécurité.' }
  }
  # planche du premontage
  $mainOut = $outFiles[-1]
  $rows = [int][math]::Ceiling($totalDur * 2 / 10)
  [void](Invoke-Ffmpeg @('-i', $mainOut, '-vf', ("fps=2,scale=135:240,tile=10x{0}" -f $rows), '-frames:v', '1', (Join-Path $ctrDir 'planche-premontage.png')) 'planche du prémontage')
  Add-Check 'OK' 'Planche du prémontage créée (une image toutes les 0,5 s) : controle\planche-premontage.png'
  # originaux intacts
  $after = $files | ForEach-Object { $f2 = Get-Item -LiteralPath $_.FullName; "{0}|{1}|{2}" -f $f2.Name, $f2.Length, $f2.LastWriteTimeUtc.Ticks }
  $same = (($before -join "`n") -eq ($after -join "`n"))
  Add-Check $(if ($same) { 'OK' } else { 'ERREUR' }) ("Rushes d'origine : nom, taille et date inchangés pour les {0} fichier(s)." -f $files.Count)
  # SRT
  $srtNote = ''
  if ($Transcription) {
    $srtTxt = [IO.File]::ReadAllText($Transcription, $utf8)
    if ($srtTxt -match '(?m)^\d+\s*\r?\n\d{2}:\d{2}:\d{2}[,.]\d{3}\s+-->\s+\d{2}:\d{2}:\d{2}[,.]\d{3}') {
      New-Item -ItemType Directory -Force -Path (Join-Path $runDir 'sous-titres') | Out-Null
      Copy-Item -LiteralPath $Transcription -Destination (Join-Path $runDir 'sous-titres\transcription.srt')
      $srtNote = 'SRT fourni par une personne, copié tel quel dans sous-titres\transcription.srt (format vérifié, contenu et synchronisation NON vérifiés).'
      Add-Todo 'Relire le SRT fourni et vérifier sa synchronisation avec la vidéo.'
    }
    else { $srtNote = 'Fichier de transcription fourni mais format SRT non reconnu : non copié.'; $script:warnings.Add($srtNote) }
  }
  else { $srtNote = "Aucun SRT de transcription : aucune transcription fiable n'est disponible (le script ne transcrit pas ; la reconnaissance vocale française n'est pas disponible sur le poste)." }
  Say ("  SRT : {0}" -f $srtNote)
}
catch [System.OperationCanceledException] {
  # arret volontaire (orientation ou plan a valider) : le rapport est quand meme ecrit
}
catch {
  $exitCode = 1
  $script:warnings.Add("ERREUR : $($_.Exception.Message)")
  Write-Host ("ERREUR : {0}" -f $_.Exception.Message) -ForegroundColor Red
}

# ================================================================== RAPPORT
if ($runDir -and (Test-Path -LiteralPath $runDir)) {
  $ctr = Join-Path $runDir 'controle'
  $sb = New-Object System.Text.StringBuilder
  $null = $sb.AppendLine("# Rapport du prémontage")
  $null = $sb.AppendLine("")
  $null = $sb.AppendLine("- Date : $(Get-Date -Format 'yyyy-MM-dd HH:mm')")
  $null = $sb.AppendLine("- Dossier de sortie : ``$runDir``")
  $etat = 'ERREUR (voir les avertissements)'
  if ($exitCode -eq 3) { $etat = 'arrêt volontaire : orientation à décider' }
  elseif ($exitCode -eq 0) {
    if ($outFiles) {
      if ($script:todo | Where-Object { $_ -like 'SORTIE NON VALID*' }) { $etat = 'terminé, SORTIE NON VALIDÉE (plan non choisi par une personne)' } else { $etat = 'terminé' }
    }
    else { $etat = 'arrêt volontaire : plan à valider par une personne' }
  }
  $null = $sb.AppendLine("- État : $etat")
  $null = $sb.AppendLine("")
  $null = $sb.AppendLine("## Commande")
  $null = $sb.AppendLine("")
  $bound = ($PSBoundParameters.GetEnumerator() | ForEach-Object { if ($_.Value -is [switch]) { "-$($_.Key)" } else { "-$($_.Key) " + (Quote-Arg ([string]$_.Value)) } }) -join ' '
  $null = $sb.AppendLine('```powershell')
  $null = $sb.AppendLine("powershell -NoProfile -ExecutionPolicy Bypass -File scripts\premontage.ps1 $bound")
  $null = $sb.AppendLine('```')
  $null = $sb.AppendLine("")
  $null = $sb.AppendLine("## Contrôles effectués par le script")
  $null = $sb.AppendLine("")
  $null = $sb.AppendLine("| État | Contrôle |")
  $null = $sb.AppendLine("| --- | --- |")
  foreach ($c in $script:checks) { $null = $sb.AppendLine("| $($c.Etat) | $(($c.Msg) -replace '\|', '/') |") }
  $null = $sb.AppendLine("")
  if ($script:warnings.Count -gt 0) {
    $null = $sb.AppendLine("## Avertissements")
    $null = $sb.AppendLine("")
    foreach ($w in $script:warnings) { $null = $sb.AppendLine("- $w") }
    $null = $sb.AppendLine("")
  }
  $null = $sb.AppendLine("## Paramètres utilisés")
  $null = $sb.AppendLine("")
  $null = $sb.AppendLine("| Paramètre | Valeur | Origine | Statut |")
  $null = $sb.AppendLine("| --- | --- | --- | --- |")
  foreach ($p in $script:paramRows) { $null = $sb.AppendLine("| $($p.Nom) | $(($p.Valeur) -replace '\|', '/') | $($p.Source) | $($p.Statut) |") }
  $null = $sb.AppendLine("")
  $null = $sb.AppendLine("Statuts : « valide » = préférence de la marque confirmée ; « essai » = valeur de cet essai, pas une règle ; « choix propre à ce fichier » = à ne pas réutiliser tel quel.")
  $null = $sb.AppendLine("")
  if ($music) {
    $null = $sb.AppendLine("## Musique")
    $null = $sb.AppendLine("")
    $null = $sb.AppendLine("- Départ : $(Fmt $music.Depart) s. $($music.Analysis.Raison)")
    $null = $sb.AppendLine("- Fondus : entrée $(Fmt $music.In) s, sortie $(Fmt $music.Out) s (niveau moyen des 1,5 dernières secondes : $($music.Analysis.NiveauFin) dB ; médiane de l'extrait : $($music.Analysis.NiveauMedian) dB).")
    $null = $sb.AppendLine("- Alignement attaques/coupes : $($music.Analysis.Alignement). Indice faible, pas une synchronisation.")
    if ($music.Analysis.Alternatives.Count -gt 0) { $null = $sb.AppendLine("- Autres départs valides : $(($music.Analysis.Alternatives | ForEach-Object { Fmt $_ }) -join ', ') s.") }
    $null = $sb.AppendLine("- Choisi sur le signal sonore, **pas à l'oreille**.")
    $null = $sb.AppendLine("")
  }
  $null = $sb.AppendLine("## Ce que le script automatise, et ce qui reste humain")
  $null = $sb.AppendLine("")
  $null = $sb.AppendLine("| Étape | Automatisé par le script | Décision ou analyse humaine nécessaire |")
  $null = $sb.AppendLine("| --- | --- | --- |")
  $null = $sb.AppendLine("| Vérification des fichiers | Oui (lecture, codec, taille, durée, rotation, son) | Non |")
  $null = $sb.AppendLine("| Orientation | Rotation lue dans le fichier si elle existe | **Sens de rotation si le fichier n'en porte pas** : regarder l'image de test |")
  $null = $sb.AppendLine("| Sélection des plans | Proposition technique seulement (netteté, ordre des noms) | **Choix réel** : pertinence, promotions, personnes, marques, qualité |")
  $null = $sb.AppendLine("| Ordre et rythme | Applique le plan fourni tel quel ; vérifie la durée cible | **Ordre, durée de chaque plan, rythme** |")
  $null = $sb.AppendLine("| Conversion, assemblage, export | Oui | Non |")
  $null = $sb.AppendLine("| Musique | Cherche un départ net par analyse du signal ; fondus ; assemblage ; niveau | **Écoute, licence, paroles, goût** |")
  $null = $sb.AppendLine("| Texte | Rendu, centrage, marges, fichiers texte | **Contenu, lisibilité réelle, test sur téléphone** |")
  $null = $sb.AppendLine("| Contrôle technique | Oui (format, durée, images noires/figées, niveau sonore, originaux intacts) | Regarder la vidéo en entier |")
  $null = $sb.AppendLine("| Sous-titres de parole (SRT) | Non (pas de transcription) ; copie un SRT fourni | **Transcription fiable** |")
  $null = $sb.AppendLine("")
  $null = $sb.AppendLine("## À vérifier par une personne")
  $null = $sb.AppendLine("")
  if ($script:todo.Count -eq 0) { $null = $sb.AppendLine("- Regarder la vidéo en entier.") } else { foreach ($t in $script:todo) { $null = $sb.AppendLine("- $t") } }
  $null = $sb.AppendLine("")
  $null = $sb.AppendLine("## SRT")
  $null = $sb.AppendLine("")
  $null = $sb.AppendLine("- $(if ($srtNote) { $srtNote } else { 'Non applicable à ce stade.' })")
  $null = $sb.AppendLine("")
  $null = $sb.AppendLine("## Fichiers produits")
  $null = $sb.AppendLine("")
  foreach ($f in (Get-ChildItem -LiteralPath $runDir -Recurse -File | Where-Object { $_.FullName -notmatch '\\_tmp\\|\\_technique\\' })) { $null = $sb.AppendLine("- ``$($f.FullName.Substring($runDir.Length + 1))``") }
  [IO.File]::WriteAllText((Join-Path $ctr 'rapport.md'), $sb.ToString(), $utf8)
  [IO.File]::WriteAllText((Join-Path $ctr 'commandes.log'), (($script:cmdLog) -join "`r`n") + "`r`n", $utf8)
  if (Test-Path -LiteralPath (Join-Path $ctr '_tmp')) { Remove-Item -LiteralPath (Join-Path $ctr '_tmp') -Recurse -Force -ErrorAction SilentlyContinue }
  Say ''
  Say ("Rapport : {0}" -f (Join-Path $ctr 'rapport.md'))
  Say ("Dossier : {0}" -f $runDir)
}
exit $exitCode
