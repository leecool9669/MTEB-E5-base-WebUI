# -*- coding: utf-8 -*-
"""
E5-base 文本嵌入 WebUI 演示
仅提供前端界面展示，不实际加载或下载模型。
"""
import gradio as gr

def load_model(model_name):
    """模拟加载模型，仅返回提示信息。"""
    if not model_name or not model_name.strip():
        return "请在输入框中填写模型名称（例如：intfloat/e5-base）后点击「加载模型」。", None
    return f"已就绪：将使用模型「{model_name.strip()}」。实际运行需在本地安装 transformers 与 torch 并联网下载权重。本演示仅展示界面。", model_name.strip()

def compute_similarity(model_state, query, *passages):
    """模拟相似度计算，返回示例表格与说明。"""
    if not query or not query.strip():
        return "请至少输入一条查询文本。", ""
    pass_list = [p.strip() for p in passages if p and p.strip()]
    if not pass_list:
        return "请至少输入一条候选段落。", ""
    # 不调用真实模型，仅生成示例展示
    header = "| 候选段落 | 相似度（示例） |\n|----------|----------------|\n"
    rows = [f"| 段落 {i+1} | 0.{85 + i % 15:.2f} |" for i in range(len(pass_list))]
    table = header + "\n".join(rows)
    msg = "当前为演示模式，未加载真实模型。上述相似度为占位示例。实际使用请先加载模型。"
    return msg, table

def create_ui():
    model_state = gr.State(value=None)

    with gr.Blocks(title="E5-base 文本嵌入 WebUI", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# E5-base 文本嵌入与相似度计算")
        gr.Markdown("输入模型名称并点击「加载模型」后，可输入查询与候选段落查看相似度展示（本演示不实际加载模型）。")

        with gr.Row():
            model_name = gr.Textbox(
                label="模型路径或名称",
                placeholder="例如：intfloat/e5-base",
                value="intfloat/e5-base",
            )
            load_btn = gr.Button("加载模型", variant="primary")
        load_status = gr.Textbox(label="加载状态", interactive=False)

        load_btn.click(
            fn=load_model,
            inputs=[model_name],
            outputs=[load_status, model_state],
        )

        gr.Markdown("---")
        gr.Markdown("### 查询与候选段落")
        query = gr.Textbox(label="查询文本", placeholder="输入查询，实际使用时建议加「query: 」前缀")
        p1 = gr.Textbox(label="候选段落 1", placeholder="输入候选文本")
        p2 = gr.Textbox(label="候选段落 2", placeholder="输入候选文本")
        p3 = gr.Textbox(label="候选段落 3", placeholder="输入候选文本（可选）")
        calc_btn = gr.Button("计算相似度", variant="secondary")

        result_msg = gr.Textbox(label="说明", interactive=False)
        result_table = gr.Markdown(label="相似度结果")

        calc_btn.click(
            fn=compute_similarity,
            inputs=[model_state, query, p1, p2, p3],
            outputs=[result_msg, result_table],
        )

    return demo

if __name__ == "__main__":
    demo = create_ui()
    demo.launch(server_name="127.0.0.1", server_port=17860)
