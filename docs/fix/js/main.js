// 语言配置
const translations = {
    en: {
        title: "ComfyUI Workflow Fixer",
        description: {
            namespace: "This tool helps fix old workflow JSON files by adding the PaintingCoder namespace to node types.",
            path: "This tool helps convert path separators between Windows (\\) and Unix-style (Linux/Mac) (/) formats."
        },
        dragText: "Choose Workflow File or drag and drop file here",
        fixButton: "Fix & Download",
        selectedFile: "Selected file: ",
        errorSelectFile: "Please select a file first.",
        successMessage: "File fixed and saved as ",
        switchLang: "中文", 
        fixTypeNamespace: "Fix PaintingCoder old version (<0.3.0) workflow",
        fixTypePath: "Fix Path Separator",
        pathOptions: {
            auto: "Auto Detect",
            toWindows: "To Windows Format (\\)",
            toUnix: "To Unix Format (Linux/Mac) (/)"
        },
        errorJsonFile: "Please select a JSON file.",
        selectedFiles: "Selected files:",
        noFilesSelected: "No files selected",
        removeFile: "Remove",
        zipOption: "Download as ZIP",
        processingFiles: "Processing {0}/{1} files...",
        successMultipleFiles: "Successfully processed {0} files",
        clearButton: "Clear All"
    },
    zh: {
        title: "ComfyUI 工作流修复工具",
        description: {
            namespace: "此工具可以通过添加 PaintingCoder 命名空间来修复旧的工作流 JSON 文件。",
            path: "此工具可以在 Windows (\\) 和 Unix (Linux/Mac) (/) 格式之间转换路径分隔符。"
        },
        dragText: "选择工作流文件或将文件拖放到此处",
        fixButton: "修复并下载",
        selectedFile: "已选择文件：",
        errorSelectFile: "请先选择一个文件。",
        successMessage: "文件已修复并保存为 ",
        switchLang: "English",
        fixTypeNamespace: "修复PaintingCoder旧版本（<0.3.0）工作流",
        fixTypePath: "修复路径分隔符",
        pathOptions: {
            auto: "自动检测",
            toWindows: "转换为 Windows 格式 (\\)",
            toUnix: "转换为 Unix 格式 (Linux/Mac) (/)"
        },
        errorJsonFile: "请选择JSON文件。",
        selectedFiles: "已选择文件：",
        noFilesSelected: "未选择文件",
        removeFile: "移除",
        zipOption: "以ZIP格式下载",
        processingFiles: "正在处理 {0}/{1} 个文件...",
        successMultipleFiles: "成功处理 {0} 个文件",
        clearButton: "清除全部"
    }
};

// 全局变量
let currentLanguage = 'en';
let currentTheme = localStorage.getItem('theme') || 'light';
let selectedFiles = [];

// 页面加载完成后的初始化
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setTheme(currentTheme);
    setupEventListeners();
    updateHeaderImage();
    initializePathOptions();
});

// 添加路径选项初始化函数
function initializePathOptions() {
    const t = translations[currentLanguage];
    
    // 初始化自动检测选项
    const autoLabel = document.getElementById('autoLabel');
    if (autoLabel) {
        autoLabel.textContent = t.pathOptions.auto;
    }
    
    // 初始化Windows格式选项
    const toWindowsLabel = document.getElementById('toWindowsLabel');
    if (toWindowsLabel) {
        toWindowsLabel.textContent = t.pathOptions.toWindows;
    }
    
    // 初始化Unix格式选项
    const toUnixLabel = document.getElementById('toUnixLabel');
    if (toUnixLabel) {
        toUnixLabel.textContent = t.pathOptions.toUnix;
    }
}

// 初始化应用
function initializeApp() {
    const urlParams = new URLSearchParams(window.location.search);
    const lang = urlParams.get('lang');
    
    if (lang && (lang === 'zh' || lang === 'en')) {
        currentLanguage = lang;
        updateLanguage();
    } else {
        const url = new URL(window.location.href);
        url.searchParams.set('lang', currentLanguage);
        window.history.replaceState({}, '', url.toString());
    }
}

// 设置事件监听器
function setupEventListeners() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    
    dropZone.addEventListener('dragover', handleDragOver);
    dropZone.addEventListener('dragleave', handleDragLeave);
    dropZone.addEventListener('drop', handleDrop);
    dropZone.addEventListener('click', () => fileInput.click());
}

// 主题切换相关函数
function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    
    const moonIcon = document.querySelector('.moon-icon');
    const sunIcon = document.querySelector('.sun-icon');
    
    if (theme === 'dark') {
        moonIcon.classList.remove('active');
        sunIcon.classList.add('active');
    } else {
        moonIcon.classList.add('active');
        sunIcon.classList.remove('active');
    }
}

function toggleTheme() {
    currentTheme = currentTheme === 'light' ? 'dark' : 'light';
    setTheme(currentTheme);
}

// 语言切换相关函数
function toggleLanguage() {
    currentLanguage = currentLanguage === 'en' ? 'zh' : 'en';
    
    const url = new URL(window.location.href);
    url.searchParams.set('lang', currentLanguage);
    window.history.replaceState({}, '', url.toString());
    
    updateLanguage();
    updateHeaderImage();
}

function updateLanguage() {
    const t = translations[currentLanguage];
    
    // 更新所有文本内容
    document.getElementById('title').textContent = t.title;
    document.getElementById('dragText').textContent = t.dragText;
    document.getElementById('fixButton').textContent = t.fixButton;
    document.getElementById('langBtn').textContent = t.switchLang;
    document.getElementById('clearButton').textContent = t.clearButton;
    document.getElementById('zipLabel').textContent = t.zipOption;
    
    // 更新下拉选项
    const fixTypeSelect = document.getElementById('fixType');
    if (fixTypeSelect) {
        const options = fixTypeSelect.options;
        options[0].textContent = t.fixTypeNamespace;
        options[1].textContent = t.fixTypePath;
    }
    
    // 更新路径选项
    initializePathOptions();
    
    updateDescription();
    updateFileList();
}

// 添加头图切换函数
function updateHeaderImage() {
    const headerImg = document.querySelector('.header-image img');
    if (headerImg) {
        const imageName = currentLanguage === 'en' ? 
            'workflow_fix_top_banner01.jpg' : 
            'workflow_fix_top_banner02.jpg';
        headerImg.src = `../images/${imageName}`;
    }
}

// 文件处理相关函数
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('dropZone').classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('dropZone').classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    const dropZone = document.getElementById('dropZone');
    dropZone.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    handleFiles(files);
}

function handleFileSelect(event) {
    handleFiles(event.target.files);
    event.target.value = '';
}

function handleFiles(files) {
    for (let file of files) {
        if (file.name.endsWith('.json')) {
            if (!selectedFiles.some(f => f.name === file.name)) {
                selectedFiles.push(file);
            }
        } else {
            const t = translations[currentLanguage];
            document.getElementById('error').textContent = t.errorJsonFile;
        }
    }
    updateFileList();
}

function updateFileList() {
    const filesContainer = document.getElementById('selectedFiles');
    const t = translations[currentLanguage];
    const clearButton = document.getElementById('clearButton');
    
    if (selectedFiles.length === 0) {
        filesContainer.innerHTML = `<div class="file-item"><span class="file-name">${t.noFilesSelected}</span></div>`;
        clearButton.disabled = true;
        document.getElementById('fixButton').disabled = true;
        filesContainer.classList.add('no-scroll');
        return;
    }
    
    filesContainer.innerHTML = selectedFiles.map((file, index) => `
        <div class="file-item">
            <span class="file-name">${file.name}</span>
            <span class="delete-btn" onclick="removeFile(${index})">×</span>
        </div>
    `).join('');
    
    // 根据文件数量控制滚动条
    if (selectedFiles.length <= 10) {
        filesContainer.classList.add('no-scroll');
    } else {
        filesContainer.classList.remove('no-scroll');
    }
    
    clearButton.disabled = false;
    document.getElementById('fixButton').disabled = false;
}

function removeFile(index) {
    selectedFiles.splice(index, 1);
    updateFileList();
}

function clearFiles() {
    selectedFiles = [];
    updateFileList();
    document.getElementById('fileInput').value = '';
    document.getElementById('error').textContent = '';
    document.getElementById('success').textContent = '';
}

// UI更新函数
function updateDescription() {
    const fixType = document.getElementById('fixType').value;
    const t = translations[currentLanguage];
    document.getElementById('description').textContent = t.description[fixType];
}

function updateUI() {
    const fixType = document.getElementById('fixType').value;
    updateDescription();
    document.getElementById('pathOptions').classList.toggle('show', fixType === 'path');
} 