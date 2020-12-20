#!/usr/bin/env pwsh

# Adds the "language" attribute that gets erased by the VSCode Python extension to kernelspec.
# Use this script if process.py (papermill) fails with AttributeError. 

$find_str = '   "display_name": "Python 3'
$replace_str = '   "language": "python", "display_name": "Python 3'

Get-ChildItem . -Filter *.ipynb |
Foreach-Object {
    If (Get-Content $_.Name -Raw | %{$_ -match $find_str}) {
        (Get-Content $_.Name -Raw) -replace $find_str, $replace_str | Set-Content -NoNewLine $_.Name
        echo "Fixed $_"
    }
}

