import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "Comfy.RandomStringSelector",
    
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "RandomStringSelector") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            nodeType.prototype.onNodeCreated = function () {
                const result = onNodeCreated?.apply(this, arguments);
                
                // 延迟初始化，确保ComfyUI完成基础设置后再添加动态输入
                setTimeout(() => {
                    const widget = this.widgets?.find(w => w.name === "input_nums");
                    const numInputs = widget ? widget.value : 3;
                    this.updateInputs(numInputs);
                }, 10);
                
                return result;
            };
            
            // 添加更新输入的方法
            nodeType.prototype.updateInputs = function(numInputs) {
                // 只删除动态添加的 string/enable 输入，不碰其他输入
                // 从后往前遍历
                for (let i = this.inputs.length - 1; i >= 0; i--) {
                    const inputName = this.inputs[i].name;
                    // 只删除 stringN 和 enableN 格式的输入
                    if (inputName.match(/^(string|enable)\d+$/)) {
                        this.removeInput(i);
                    }
                }
                
                // 添加新的动态输入
                for (let i = 1; i <= numInputs; i++) {
                    this.addInput(`string${i}`, "STRING");
                    this.addInput(`enable${i}`, "BOOLEAN");
                }
                
                this.setSize(this.computeSize());
            };
            
            // 监听输入变化
            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
                const result = onConnectionsChange?.apply(this, arguments);
                
                // 检查是否是input_nums参数变化
                if (index === 0 && type === 1) { // input_nums是第一个输入
                    const widget = this.widgets?.find(w => w.name === "input_nums");
                    if (widget) {
                        this.updateInputs(widget.value);
                    }
                }
                
                return result;
            };
            
            // 监听widget值变化
            const onWidgetChanged = nodeType.prototype.onWidgetChanged;
            nodeType.prototype.onWidgetChanged = function(name, value, old_value) {
                const result = onWidgetChanged?.apply(this, arguments);
                
                if (name === "input_nums") {
                    this.updateInputs(value);
                }
                
                return result;
            };
        }
    }
});

