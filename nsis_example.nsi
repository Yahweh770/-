; Пример скрипта для NSIS (Nullsoft Scriptable Install System)
; Демонстрирует структуру настоящего установщика

; Установка базовых параметров
Name "My Application"
OutFile "MyApp_Installer.exe"
InstallDir $PROGRAMFILES\MyApplication
RequestExecutionLevel admin

; Включение страниц установщика
Page license
Page components
Page directory
Page instfiles
UninstPage uninstConfirm
UninstPage instfiles

; Лицензионное соглашение
LicenseText "Please read the following license agreement carefully"
LicenseData "license.txt"  ; файл с текстом лицензии

; Компоненты для установки
Section "Main Application" SecMain
    SectionIn RO  ; обязательный компонент
    SetOutPath $INSTDIR
    File /r "app_files\*.*"  ; копирование файлов приложения
    
    ; Создание ярлыков
    CreateShortCut "$DESKTOP\MyApplication.lnk" "$INSTDIR\main.exe"
    CreateShortCut "$SMPROGRAMS\MyApplication\MyApplication.lnk" "$INSTDIR\main.exe"
    CreateShortCut "$SMPROGRAMS\MyApplication\Uninstall.lnk" "$INSTDIR\uninstall.exe"
    
    ; Регистрация в системе
    WriteUninstaller "$INSTDIR\uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\MyApplication" \
                     "DisplayName" "My Application"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\MyApplication" \
                     "UninstallString" "$INSTDIR\uninstall.exe"
SectionEnd

; Дополнительный компонент (опционально)
Section "Documentation" SecDocs
    SetOutPath "$INSTDIR\docs"
    File /r "docs\*.*"
SectionEnd

; Установка параметров по умолчанию
SectionGroup /e "Startup Options" SecGroup
    Section "Launch My Application" SecLaunch
        ; Запуск приложения после установки
        Exec "$INSTDIR\main.exe"
    SectionEnd
SectionGroupEnd

; Действия при установке
Function .onInstSuccess
    MessageBox MB_YESNO "Do you want to read the README file now?" IDYES readme
    Goto end
    readme:
        Exec "notepad.exe $INSTDIR\README.txt"
    end:
FunctionEnd

; Деинсталлятор
Section "Uninstall"
    Delete "$INSTDIR\*.*"
    RMDir /r "$INSTDIR"
    Delete "$DESKTOP\MyApplication.lnk"
    Delete "$SMPROGRAMS\MyApplication\*.*"
    RMDir "$SMPROGRAMS\MyApplication"
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\MyApplication"
SectionEnd