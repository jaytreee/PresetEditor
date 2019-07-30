set Path=%Path%;C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64;C:\Program Files (x86)\Microsoft SDKs\NuGetPackages\Microsoft.NETCore.Windows.ApiSets-x64\1.0.0\runtimes\win7-x64\native
pyinstaller --debug all preset_editor.spec
pause