#!/usr/bin/env python
# coding=utf-8
# Copyright 2024 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import mimetypes
import os
import re
import shutil
from typing import Optional

# Replace smolagents imports with simple implementations
class AgentAudio:
    def to_string(self):
        return "Audio output not available"

class AgentImage:
    def to_string(self):
        return "Image output not available"

class AgentText:
    def __init__(self, text):
        self.text = text
    
    def to_string(self):
        return self.text

class ActionStep:
    def __init__(self, step_number=None):
        self.step_number = step_number
        self.model_output = None
        self.tool_calls = None
        self.observations = None
        self.error = None
        self.input_token_count = 0
        self.output_token_count = 0
        self.duration = 0

class MemoryStep:
    pass

class MultiStepAgent:
    pass

def handle_agent_output_types(output):
    if isinstance(output, str):
        return AgentText(output)
    return output

def _is_package_available(package_name):
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def pull_messages_from_step(
    step_log: MemoryStep,
):
    """Extract ChatMessage objects from agent steps with proper nesting"""
    import gradio as gr

    if isinstance(step_log, ActionStep):
        # Output the step number
        step_number = f"Step {step_log.step_number}" if step_log.step_number is not None else ""
        yield {"role": "assistant", "content": f"**{step_number}**"}

        # First yield the thought/reasoning from the LLM
        if hasattr(step_log, "model_output") and step_log.model_output is not None:
            # Clean up the LLM output
            model_output = step_log.model_output.strip()
            # Remove any trailing <end_code> and extra backticks, handling multiple possible formats
            model_output = re.sub(r"```\s*<end_code>", "```", model_output)  # handles ```<end_code>
            model_output = re.sub(r"<end_code>\s*```", "```", model_output)  # handles <end_code>```
            model_output = re.sub(r"```\s*\n\s*<end_code>", "```", model_output)  # handles ```\n<end_code>
            model_output = model_output.strip()
            yield {"role": "assistant", "content": model_output}

        # For tool calls, create a parent message
        if hasattr(step_log, "tool_calls") and step_log.tool_calls is not None:
            first_tool_call = step_log.tool_calls[0]
            used_code = first_tool_call.name == "python_interpreter"
            parent_id = f"call_{len(step_log.tool_calls)}"

            # Tool call becomes the parent message with timing info
            # First we will handle arguments based on type
            args = first_tool_call.arguments
            if isinstance(args, dict):
                content = str(args.get("answer", str(args)))
            else:
                content = str(args).strip()

            if used_code:
                # Clean up the content by removing any end code tags
                content = re.sub(r"```.*?\n", "", content)  # Remove existing code blocks
                content = re.sub(r"\s*<end_code>\s*", "", content)  # Remove end_code tags
                content = content.strip()
                if not content.startswith("```python"):
                    content = f"```python\n{content}\n```"

            parent_message_tool = {
                "role": "assistant",
                "content": content,
                "metadata": {
                    "title": f"🛠️ Used tool {first_tool_call.name}",
                    "id": parent_id,
                    "status": "pending",
                },
            }
            yield parent_message_tool

            # Nesting execution logs under the tool call if they exist
            if hasattr(step_log, "observations") and (
                step_log.observations is not None and step_log.observations.strip()
            ):  # Only yield execution logs if there's actual content
                log_content = step_log.observations.strip()
                if log_content:
                    log_content = re.sub(r"^Execution logs:\s*", "", log_content)
                    yield {
                        "role": "assistant",
                        "content": f"{log_content}",
                        "metadata": {"title": "📝 Execution Logs", "parent_id": parent_id, "status": "done"},
                    }

            # Nesting any errors under the tool call
            if hasattr(step_log, "error") and step_log.error is not None:
                yield {
                    "role": "assistant",
                    "content": str(step_log.error),
                    "metadata": {"title": "💥 Error", "parent_id": parent_id, "status": "done"},
                }

            # Update parent message metadata to done status without yielding a new message
            parent_message_tool["metadata"]["status"] = "done"

        # Handle standalone errors but not from tool calls
        elif hasattr(step_log, "error") and step_log.error is not None:
            yield {"role": "assistant", "content": str(step_log.error), "metadata": {"title": "💥 Error"}}

        # Calculate duration and token information
        step_footnote = f"{step_number}"
        if hasattr(step_log, "input_token_count") and hasattr(step_log, "output_token_count"):
            token_str = (
                f" | Input-tokens:{step_log.input_token_count:,} | Output-tokens:{step_log.output_token_count:,}"
            )
            step_footnote += token_str
        if hasattr(step_log, "duration"):
            if step_log.duration:
                step_duration = f" | Duration: {round(float(step_log.duration), 2)}"
                step_footnote += step_duration
        step_footnote = f"""<span style="color: #bbbbc2; font-size: 12px;">{step_footnote}</span> """
        yield {"role": "assistant", "content": f"{step_footnote}"}
        yield {"role": "assistant", "content": "-----"}


def stream_to_gradio(
    agent,
    task: str,
    reset_agent_memory: bool = False,
    additional_args: Optional[dict] = None,
):
    """
    Stream agent responses to Gradio.
    """
    if not _is_package_available("gradio"):
        raise ModuleNotFoundError(
            "Please install 'gradio' extra to use the GradioUI: `pip install 'gradio'`"
        )
    import gradio as gr

    try:
        # Special handling for greetings
        greeting_patterns = ["hi", "hello", "hey", "greetings", "howdy"]
        if task.lower().strip() in greeting_patterns or task.lower().strip() + "!" in greeting_patterns:
            yield {"role": "assistant", "content": "Hello! I'm your USA Travel Guide Assistant. How can I help you plan your trip today? I can provide information about destinations, accommodation, transportation, attractions, and more!"}
            return
        
        # Actual implementation using the agent
        if reset_agent_memory:
            agent.memory.reset()
            
        # Run the agent on the task
        response = agent.run(task, additional_args=additional_args)
        
        # Process each step from the agent's memory
        for step_log in agent.memory.steps:
            for message in pull_messages_from_step(step_log):
                yield message
                
        # Final answer if available
        if hasattr(agent, "final_answer") and agent.final_answer:
            yield {"role": "assistant", "content": f"**Final answer:**\n{agent.final_answer}\n"}
        else:
            # Include the response from agent.run as a fallback if final_answer isn't available
            if response:
                yield {"role": "assistant", "content": f"{response}"}
            else:
                yield {"role": "assistant", "content": "I processed your request, but couldn't generate a final answer. Can you provide more details or ask your question differently?"}
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in agent interaction: {str(e)}")
        print(f"Error details: {error_details}")
        
        # Provide a user-friendly error message
        if "final_answer" in str(e):
            yield {"role": "assistant", "content": "I'm having trouble processing your request. Let me try a simpler response: How can I help you plan your USA trip today?"}
        else:
            yield {"role": "assistant", "content": f"I encountered an error while processing your request. Please try again with a more specific travel-related question."}


class GradioUI:
    """A one-line interface to launch your agent in Gradio"""

    def __init__(self, agent: MultiStepAgent, file_upload_folder: str | None = None):
        if not _is_package_available("gradio"):
            raise ModuleNotFoundError(
                "Please install 'gradio' extra to use the GradioUI: `pip install 'gradio'`"
            )
        self.agent = agent
        self.file_upload_folder = file_upload_folder
        if self.file_upload_folder is not None:
            if not os.path.exists(file_upload_folder):
                os.mkdir(file_upload_folder)

    def interact_with_agent(self, prompt, messages):
        import gradio as gr

        messages.append({"role": "user", "content": prompt})
        yield messages
        for msg in stream_to_gradio(self.agent, task=prompt, reset_agent_memory=False):
            messages.append(msg)
            yield messages
        yield messages

    def upload_file(
        self,
        file,
        file_uploads_log,
        allowed_file_types=[
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain",
        ],
    ):
        """
        Handle file uploads, default allowed types are .pdf, .docx, and .txt
        """
        import gradio as gr

        if file is None:
            return gr.Textbox(value="No file uploaded", visible=True), file_uploads_log

        try:
            mime_type, _ = mimetypes.guess_type(file.name)
        except Exception as e:
            return gr.Textbox(value=f"Error: {e}", visible=True), file_uploads_log

        if mime_type not in allowed_file_types:
            return gr.Textbox(value="File type disallowed", visible=True), file_uploads_log

        # Sanitize file name
        original_name = os.path.basename(file.name)
        sanitized_name = re.sub(
            r"[^\w\-.]", "_", original_name
        )  # Replace any non-alphanumeric, non-dash, or non-dot characters with underscores

        type_to_ext = {}
        for ext, t in mimetypes.types_map.items():
            if t not in type_to_ext:
                type_to_ext[t] = ext

        # Ensure the extension correlates to the mime type
        sanitized_name = sanitized_name.split(".")[:-1]
        sanitized_name.append("" + type_to_ext[mime_type])
        sanitized_name = "".join(sanitized_name)

        # Save the uploaded file to the specified folder
        file_path = os.path.join(self.file_upload_folder, os.path.basename(sanitized_name))
        shutil.copy(file.name, file_path)

        return gr.Textbox(value=f"File uploaded: {file_path}", visible=True), file_uploads_log + [file_path]

    def log_user_message(self, text_input, file_uploads_log):
        return (
            text_input
            + (
                f"\nYou have been provided with these files, which might be helpful or not: {file_uploads_log}"
                if len(file_uploads_log) > 0
                else ""
            ),
            "",
        )

    def launch(self, **kwargs):
        import gradio as gr

        with gr.Blocks() as demo:
            stored_messages = gr.State([])
            file_uploads_log = gr.State([])
            chatbot = gr.Chatbot(
                label="Agent",
                avatar_images=(
                    None,
                    "https://huggingface.co/datasets/agents-course/course-images/resolve/main/en/communication/Alfred.png",
                ),
                scale=1,
                type='messages'
            )
            # If an upload folder is provided, enable the upload feature
            if self.file_upload_folder is not None:
                upload_file = gr.File(label="Upload a file")
                upload_status = gr.Textbox(label="Upload Status", interactive=False, visible=False)
                upload_file.change(
                    self.upload_file,
                    [upload_file, file_uploads_log],
                    [upload_status, file_uploads_log],
                )
            text_input = gr.Textbox(lines=1, label="Chat Message")
            text_input.submit(
                self.log_user_message,
                [text_input, file_uploads_log],
                [stored_messages, text_input],
            ).then(self.interact_with_agent, [stored_messages, chatbot], [chatbot])

        demo.launch(debug=True, **kwargs)


__all__ = ["stream_to_gradio", "GradioUI"]