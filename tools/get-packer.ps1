[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$latestVersion = [string](((Invoke-RestMethod -Uri https://releases.hashicorp.com/packer/) -split "\n" | select-string -pattern "(\d+\.){2,3}\d+" | foreach {$_.matches} | select -expandproperty value) | %{[System.Version]$_} | sort | select -last 1)
Write-Host "Latest version is $latestVersion"
$url = "https://releases.hashicorp.com/packer/$latestVersion/packer_${latestVersion}_windows_amd64.zip"
Write-Host "Download link is $url"
$output = "$PSScriptRoot\packer.zip"

Write-Host "Going to start download"
(New-Object System.Net.WebClient).DownloadFile($url, $output)
Write-Host "Finished download. Going to unzip"
$extractPath = (get-item $PSScriptRoot).parent.FullName
$shell = new-object -com shell.application
$zip = $shell.NameSpace($output)
foreach($item in $zip.items()) {
	$shell.Namespace("$extractPath").copyhere($item)
}