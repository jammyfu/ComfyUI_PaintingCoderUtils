import { app } from "/scripts/app.js";

app.registerExtension({
    name: "Comfy.PaintingCoder.DynamicMaskCombiner",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // 检查是否为 DynamicMaskCombiner 节点
        if (nodeData.name === "DynamicMaskCombiner") {
            // 保存原始的 onNodeCreated 方法
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            // 重写 onNodeCreated 方法
            nodeType.prototype.onNodeCreated = function() {
                const result = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                // 初始化连接计数器
                this.lastConnectedCount = 0;
                // 添加第一个掩码输入
                this.addInput("mask_1", "MASK");
                return result;
            };

            // 处理连接变化的方法
            nodeType.prototype.onConnectionsChange = function(connectionType, slot, isConnected) {
                // 只处理输入连接的变化
                if (connectionType === 1) {
                    // 计算当前已连接的掩码输入数量
                    const connectedCount = this.inputs.reduce((count, input) => 
                        input.name.startsWith('mask_') ? (count + (input.link ? 1 : 0)) : count, 0);

                    // 如果连接数量发生变化
                    if (connectedCount !== this.lastConnectedCount) {
                        this.lastConnectedCount = connectedCount;
                        const targetCount = Math.max(connectedCount + 1, 1); // 确保至少保留一个输入

                        // 获取所有mask输入
                        const maskInputs = this.inputs
                            .map((input, index) => ({ index, name: input.name }))
                            .filter(input => input.name.startsWith('mask_'));

                        // 添加新的输入槽位
                        if (maskInputs.length < targetCount) {
                            const newIndex = maskInputs.length + 1;
                            this.addInput(`mask_${newIndex}`, "MASK");
                        }

                        // 只在确实需要移除时才移除多余的输入槽位
                        if (maskInputs.length > targetCount) {
                            // 从后向前检查未连接的输入
                            for (let i = maskInputs.length - 1; i >= targetCount; i--) {
                                const input = this.inputs[maskInputs[i].index];
                                if (!input.link) {
                                    this.removeInput(maskInputs[i].index);
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