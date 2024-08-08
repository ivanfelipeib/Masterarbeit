# -*- mode: python ; coding: utf-8 -*-

import PyInstaller.config
import os

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[
        '.',
        'Operations'
        ],
    binaries=[('ConsoleIdsAudit/ConsoleIdsAudit.exe', 'ConsoleIdsAudit')],
    datas=[
        ('GUI_windows/*', 'GUI_Windows'),
        ('GUI_windows/Filters-Requirements/*', 'GUI_Windows/Filters-Requirements'),
        ('temp_files/*', 'temp_files'),

        (r'C:\Users\ivanf\OneDrive\Desktop\Masterarbeit\0-Repo_Thesis\.venv\Lib\site-packages\xmlschema\schemas\XSD_1.0\*','xmlschema\\schemas\\XSD_1.0'),
        (r'C:\Users\ivanf\OneDrive\Desktop\Masterarbeit\0-Repo_Thesis\.venv\Lib\site-packages\xmlschema\schemas\XSD_1.1\*','xmlschema\\schemas\\XSD_1.1'),
        (r'C:\Users\ivanf\OneDrive\Desktop\Masterarbeit\0-Repo_Thesis\.venv\Lib\site-packages\xmlschema\schemas\VC\XMLSchema-versioning.xsd','xmlschema\\schemas\\VC'),
        (r'C:\Users\ivanf\OneDrive\Desktop\Masterarbeit\0-Repo_Thesis\.venv\Lib\site-packages\xmlschema\schemas\XSI\XMLSchema-instance_minimal.xsd','xmlschema\\schemas\\XSI'),
        (r'C:\Users\ivanf\OneDrive\Desktop\Masterarbeit\0-Repo_Thesis\.venv\Lib\site-packages\xmlschema\schemas\XML\xml_minimal.xsd','xmlschema\\schemas\\XML'),

        (r'C:\Users\ivanf\OneDrive\Desktop\Masterarbeit\0-Repo_Thesis\.venv\Lib\site-packages\ifctester\*','ifctester'),
        (r'C:\Users\ivanf\OneDrive\Desktop\Masterarbeit\0-Repo_Thesis\.venv\Lib\site-packages\ifctester\templates\*','ifctester\\templates'),
        (r'C:\Users\ivanf\OneDrive\Desktop\Masterarbeit\0-Repo_Thesis\.venv\Lib\site-packages\ifcopenshell\express\*','ifcopenshell\\express'),
        (r'C:\Users\ivanf\OneDrive\Desktop\Masterarbeit\0-Repo_Thesis\.venv\Lib\site-packages\ifcopenshell\express\rules*','ifcopenshell\\express\\rules')
    ],
    hiddenimports=[
        'xmlschema',
        'ifcopenshell.express',

    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='BIM_Quick_Checker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BIM_Quick_Checker'
)
