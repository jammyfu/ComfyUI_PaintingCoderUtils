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
                    // 从第三个开始删除
                    for (let i = 2; i < this.widgets.length; i++) {
                        this.widgets[i].onRemove?.();
                    }
                    this.widgets.length = 2;
                }

                // 处理文本数组
                const v = Array.isArray(text) ? text : [...text]; // 确保 text 是数组
                if (v.length > 0 && !v[0]) { // 处理第一个元素为空字符串的情况
                    v.shift();
                }

                // 获取显示开关状态
                const showOutput = this.widgets[1].value;

                // 为每个文本创建widget
                v.forEach((list, index) => {
                    console.log(`[ShowTextPlus] Creating widget ${index + 1} for:`, list);
                    const w = ComfyWidgets["STRING"](
                        this,
                        `text_output_${index}`, // 为每个文本输出widget设置不同的name
                        ["STRING", { multiline: true }],
                        app
                    ).widget;
                    w.inputEl.readOnly = true;
                    w.inputEl.style.opacity = 0.6;
                    w.value = list;
                    // 根据开关状态设置显示
                    updateWidgetDisplay(w, showOutput);
                });

                // 调整节点大小
                 requestAnimationFrame(() => {
                    adjustNodeSize.call(this);
                 });
            }


             function updateWidgetDisplay(widget, show) {
                if (widget && widget.inputEl) {
                    widget.inputEl.style.display = show ? "block" : "none";
                    widget.inputEl.style.visibility = show ? "visible" : "hidden";

                    // 尝试手动触发大小计算
                    if (!show) {
                        widget.inputEl.style.height = "0px"
                        widget.inputEl.style.padding = "0px";
                        // 设置高度为 0， 并移除padding
                    } else {
                        widget.inputEl.style.height = "";
                        widget.inputEl.style.padding = "";
                    }
                    // 动态计算并设置文本框的高度，修复高度设置为0px之后不能完全展开的问题
                    requestAnimationFrame(() => {
                        if(show){
                             widget.inputEl.style.height = `${widget.inputEl.scrollHeight}px`;
                        }
                    });
                }
            }

            function adjustNodeSize() {
                const sz = this.computeSize();
                if (sz[0] < this.size[0]) {
                    sz[0] = this.size[0];
                }
                if (sz[1] < this.size[1]) {
                    sz[1] = this.size[1];
                }
                this.onResize?.(sz);
                app.graph.setDirtyCanvas(true, false);
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
                            updateWidgetDisplay(this.widgets[i], value);
                        }
                    }

                    // 重新计算节点大小
                     requestAnimationFrame(() => {
                        adjustNodeSize.call(this);
                     });
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
                // 在执行完成后调整节点大小
                requestAnimationFrame(() => {
                      adjustNodeSize.call(this);
                });
            };


            // 加载时恢复显示
            const onConfigure = nodeType.prototype.onConfigure;
            nodeType.prototype.onConfigure = function () {
               console.log("[ShowTextPlus] Node configured, values:", this.widgets_values);
               onConfigure?.apply(this, arguments);
                if (this.widgets_values?.length) {
                   console.log("[ShowTextPlus] Restoring from config:", this.widgets_values);
                   const textValues = this.widgets_values.slice(1); //从第二个值开始，跳过toggle
                    populate.call(this, textValues);
                }
                // 在配置完成后调整节点大小
               requestAnimationFrame(() => {
                    adjustNodeSize.call(this);
               });
           };
        }
    },
});
