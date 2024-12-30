import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

app.registerExtension({
    name: "PaintingCoder.ShowTextPlus",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        console.log("[ShowTextPlus] Registering node:", nodeData.name);

        if (nodeData.name === "ShowTextPlus") {
            function populate(text) {
                console.log("[ShowTextPlus] Populating with:", text);
                
                // 清理现有widgets（保留第一个输入框和显示开关）
                if (this.widgets) {
                    for (let i = 2; i < this.widgets.length; i++) {  // 从2开始，保留前两个widget
                        this.widgets[i].onRemove?.();
                    }
                    this.widgets.length = 2;  // 保留前两个widget
                }

                // 处理文本数组
                const v = [...text];
                if (!v[0]) {
                    v.shift();
                }

                // 获取显示开关状态
                const showOutput = this.widgets[1].value;  // 第二个widget是显示开关

                // 为每个文本创建widget
                for (const list of v) {
                    console.log("[ShowTextPlus] Creating widget for:", list);
                    const w = ComfyWidgets["STRING"](
                        this,
                        "text2",
                        ["STRING", { multiline: true }],
                        app
                    ).widget;
                    w.inputEl.readOnly = true;
                    w.inputEl.style.opacity = 0.6;
                    w.value = list;
                    // 根据开关状态设置显示
                    w.inputEl.style.display = showOutput ? "block" : "none";
                }

                // 调整节点大小
                requestAnimationFrame(() => {
                    const sz = this.computeSize();
                    if (sz[0] < this.size[0]) {
                        sz[0] = this.size[0];
                    }
                    if (sz[1] < this.size[1]) {
                        sz[1] = this.size[1];
                    }
                    this.onResize?.(sz);
                    app.graph.setDirtyCanvas(true, false);
                });
            }

            // 添加显示开关的创建
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                onNodeCreated?.apply(this, arguments);
                
                // 添加显示开关
                this.addWidget("toggle", "show_output", true, (value) => {
                    console.log("[ShowTextPlus] Toggle output display:", value);
                    // 更新所有输出文本框的显示状态
                    for (let i = 2; i < this.widgets.length; i++) {
                        if (this.widgets[i].inputEl) {
                            this.widgets[i].inputEl.style.display = value ? "block" : "none";
                        }
                    }
                    // 重新计算节点大小
                    this.onResize?.(this.computeSize());
                    app.graph.setDirtyCanvas(true, false);
                });
            };

            // 执行时更新显示
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                console.log("[ShowTextPlus] Node executed, message:", message);
                onExecuted?.apply(this, arguments);
                if (message?.text) {
                    console.log("[ShowTextPlus] Updating from execution:", message.text);
                    populate.call(this, message.text);
                }
            };

            // 加载时恢复显示
            const onConfigure = nodeType.prototype.onConfigure;
            nodeType.prototype.onConfigure = function () {
                console.log("[ShowTextPlus] Node configured, values:", this.widgets_values);
                onConfigure?.apply(this, arguments);
                if (this.widgets_values?.length) {
                    console.log("[ShowTextPlus] Restoring from config:", this.widgets_values);
                    populate.call(this, this.widgets_values.slice(+this.widgets_values.length > 1));
                }
            };
        }
    },
}); 