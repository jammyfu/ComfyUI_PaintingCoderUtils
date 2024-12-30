import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

app.registerExtension({
    name: "PaintingCoder.ShowTextPlus",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        console.log("[ShowTextPlus] Registering node:", nodeData.name);

        if (nodeData.name === "ShowTextPlus") {
            function populate(text) {
                console.log("[ShowTextPlus] Populating with:", text);
                
                // 清理现有widgets
                if (this.widgets) {
                    for (let i = 1; i < this.widgets.length; i++) {
                        this.widgets[i].onRemove?.();
                    }
                    this.widgets.length = 1;
                }

                // 处理文本数组
                const v = [...text];
                if (!v[0]) {
                    v.shift();
                }

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