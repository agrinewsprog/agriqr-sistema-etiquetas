; Script de Inno Setup para Sistema de Etiquetas AgriQR
; Incluye la app corporativa y los drivers Brother QL Series
[Setup]
AppName=Sistema de Etiquetas AgriQR
AppVersion=2.0
AppPublisher=AgriNews
AppPublisherURL=https://agrinews.com
DefaultDirName={pf}\SistemaEtiquetasAgriQR
DefaultGroupName=Sistema de Etiquetas AgriQR
OutputDir=.
OutputBaseFilename=SistemaEtiquetasAgriQR_Installer
Compression=lzma
SolidCompression=yes
SetupIconFile=icono-agriQR.ico
UninstallDisplayIcon={app}\SistemaEtiquetasAgriQR.exe

[Files]
Source: "dist\SistemaEtiquetasAgriQR.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icono-agriQR.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "configurar_impresora.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "QL600_Driver.exe"; DestDir: "{tmp}"; Flags: ignoreversion
Source: "QL700_Driver.exe"; DestDir: "{tmp}"; Flags: ignoreversion
Source: "QL800_Driver.exe"; DestDir: "{tmp}"; Flags: ignoreversion

[Icons]
Name: "{group}\Sistema de Etiquetas AgriQR"; Filename: "{app}\SistemaEtiquetasAgriQR.exe"; IconFilename: "{app}\icono-agriQR.ico"
Name: "{commondesktop}\Sistema de Etiquetas AgriQR"; Filename: "{app}\SistemaEtiquetasAgriQR.exe"; IconFilename: "{app}\icono-agriQR.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Accesos directos adicionales:"

[Components]
Name: "ql600"; Description: "Instalar driver Brother QL-600"; Types: custom full
Name: "ql700"; Description: "Instalar driver Brother QL-700"; Types: custom full  
Name: "ql800"; Description: "Instalar driver Brother QL-800"; Types: custom full

[Run]
Filename: "{tmp}\QL600_Driver.exe"; Description: "Instalar driver Brother QL-600"; Flags: waituntilterminated; Components: ql600
Filename: "{tmp}\QL700_Driver.exe"; Description: "Instalar driver Brother QL-700"; Flags: waituntilterminated; Components: ql700
Filename: "{tmp}\QL800_Driver.exe"; Description: "Instalar driver Brother QL-800"; Flags: waituntilterminated; Components: ql800
; Ejecutar el programa después de la instalación
Filename: "{app}\SistemaEtiquetasAgriQR.exe"; Description: "Iniciar Sistema de Etiquetas AgriQR"; Flags: postinstall nowait skipifsilent
