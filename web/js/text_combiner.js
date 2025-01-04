import { app } from "/scripts/app.js";

app.registerExtension({
    name: "Comfy.PaintingCoder.TextCombiner",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // 检查是否为 TextCombiner 节点
        if (nodeData.name === "TextCombiner") {
            // 添加自定义样式
            const style = document.createElement('style');
            style.textContent = `
                // 节点基本样式
                .comfy-node[data-type="TextCombiner"] {
                    background-color: rgb(63, 77, 85) !important;
                    color: rgb(255, 255, 255) !important;
                }

                // 标题栏样式
                .comfy-node[data-type="TextCombiner"] .title-box {
                    background-color: rgb(45, 55, 65) !important;
                    color: rgb(33, 37, 41) !important;
                }

                // 悬停效果
                .comfy-node[data-type="TextCombiner"]:hover {
                    background-color: rgba(63, 77, 85, 0.9) !important;
                }
            `;
            document.head.appendChild(style);

            // 保存原始的 onNodeCreated 方法
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            // 重写 onNodeCreated 方法
            nodeType.prototype.onNodeCreated = function() {
                const result = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                // 初始化连接计数器
                this.lastConnectedCount = 0;
                // 添加第一个文本输入
                this.addInput("text_1", "STRING");
                
                // 设置节点颜色
                if (this.constructor.nodeData?.name === "TextCombiner") {
                    this.bgcolor = "#2e414a";
                    this.color = "#132832"; 
                    if (this.title_box) {
                        this.title_box.style.backgroundColor = "rgb(45, 55, 65)";
                        this.title_box.style.color = "#212529";
                    }
                }
                
                return result;
            };

            // 处理连接变化的方法
            nodeType.prototype.onConnectionsChange = function(connectionType, slot, isConnected) {
                // 只处理输入连接的变化
                if (connectionType === 1) {
                    // 计算当前已连接的文本输入数量
                    const connectedCount = this.inputs.reduce((count, input) => 
                        input.name.startsWith('text_') ? (count + (input.link ? 1 : 0)) : count, 0);

                    // 如果连接数量发生变化
                    if (connectedCount !== this.lastConnectedCount) {
                        this.lastConnectedCount = connectedCount;
                        const targetCount = Math.max(connectedCount + 1, 1); // 确保至少保留一个输入

                        // 获取所有text输入
                        const textInputs = this.inputs
                            .map((input, index) => ({ index, name: input.name }))
                            .filter(input => input.name.startsWith('text_'));

                        // 添加新的输入槽位
                        if (textInputs.length < targetCount) {
                            const newIndex = textInputs.length + 1;
                            this.addInput(`text_${newIndex}`, "STRING");
                        }

                        // 只在确实需要移除时才移除多余的输入槽位
                        if (textInputs.length > targetCount) {
                            // 从后向前检查未连接的输入
                            for (let i = textInputs.length - 1; i >= targetCount; i--) {
                                const input = this.inputs[textInputs[i].index];
                                if (!input.link) {
                                    this.removeInput(textInputs[i].index);
                                }
                            }
                        }

                        // 更新节点大小和画布
                        this.setSize(this.computeSize());
                        app.graph.setDirtyCanvas(true);
                    }
                }
            };
        }
    }
});