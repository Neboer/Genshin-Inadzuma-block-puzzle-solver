python $(Join-Path -Path $PSScriptRoot -ChildPath "solvercli.py")
Write-Host -NoNewLine 'Press any key to continue...';
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');