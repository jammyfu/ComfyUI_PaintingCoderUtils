import { app } from "/scripts/app.js";

app.registerExtension({
    name: "Comfy.PaintingCoder.TextCombiner",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "TextCombiner") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                const result = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                // 初始化状态
                this.lastConnectedCount = 0;
                
                // 添加第一个输入点
                console.log("初始化：添加第一个输入点");
                this.addInput("text_1", "STRING");
                
                return result;
            };

            nodeType.prototype.onConnectionsChange = function(connectionType, slot, isConnected) {
                if (connectionType === 1) {  // 输入连接
                    console.log(`连接变化 - 槽位: ${slot}, 已连接: ${isConnected}`);
                    
                    const connectedCount = this.inputs.reduce((count, input) => 
                        count + (input.link ? 1 : 0), 0);
                    
                    console.log(`当前连接数量: ${connectedCount}, 上次连接数量: ${this.lastConnectedCount}`);

                    if (connectedCount !== this.lastConnectedCount) {
                        this.lastConnectedCount = connectedCount;
                        const targetCount = connectedCount + 1;
                        console.log(`目标输入点数量: ${targetCount}`);

                        while (this.inputs.length < targetCount) {
                            const newIndex = this.inputs.length + 1;
                            console.log(`添加新输入点: text_${newIndex}`);
                            this.addInput(`text_${newIndex}`, "STRING");
                        }

                        while (this.inputs.length > Math.max(targetCount, 1)) {
                            const lastInput = this.inputs[this.inputs.length - 1];
                            if (!lastInput.link) {
                                console.log(`移除输入点: ${this.inputs.length}`);
                                this.removeInput(this.inputs.length - 1);
                            }
                        }

                        console.log(`更新节点大小，当前输入点数量: ${this.inputs.length}`);
                        this.setSize(this.computeSize());
                        app.graph.setDirtyCanvas(true);
                    }
                }
            };
        }
    }
});