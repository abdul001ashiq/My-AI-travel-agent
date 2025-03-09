# Deploying to Hugging Face Spaces

This guide will help you deploy your USA Travel Guide AI Assistant to Hugging Face Spaces so you can share it on LinkedIn.

## Step 1: Create a Hugging Face Account

1. Go to [Hugging Face](https://huggingface.co/) and sign up for an account if you don't have one
2. Make sure you have a valid API token with READ access (or higher)

## Step 2: Create a New Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create a new Space"
3. Enter a name for your Space (e.g., "usa-travel-guide")
4. Select "Gradio" as the SDK
5. Choose "Public" visibility (important for LinkedIn sharing)
6. Click "Create Space"

## Step 3: Add Your Hugging Face Token as a Secret

1. Go to your Space settings
2. Scroll down to "Repository secrets"
3. Add a new secret:
   - Name: `HUGGING_FACE_TOKEN`
   - Value: Your Hugging Face token
4. Save the secret

## Step 4: Upload Your Files

You can upload files through the web interface or use Git:

### Option 1: Web Interface (Easiest)
1. Click "Files" in your Space
2. Click "Add file" and upload each of these files:
   - app.py
   - Gradio_UI.py
   - prompts.yaml
   - requirements.txt
   - README.md
   - .gitattributes
   - Any data folders
3. Make sure to maintain the directory structure

### Option 2: Git (More Control)
1. Clone your Space repository:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
   ```
2. Copy your project files to the cloned repository
3. Commit and push:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push
   ```

## Step 5: Wait for Deployment

Your Space will automatically build and deploy. This may take several minutes, especially on the first build.

## Step 6: Test Your Deployment

1. Once deployed, you'll see the Gradio interface on your Space URL:
   ```
   https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
   ```
2. Test the assistant with various travel-related questions
3. Make sure it's working as expected


## Troubleshooting

If you encounter issues:

1. **Build Errors**: Check the build logs in your Space for detailed error messages
2. **Missing Dependencies**: Make sure all required packages are listed in requirements.txt
3. **Token Issues**: Verify your Hugging Face token has the correct permissions
4. **Model Errors**: If the model isn't working, try falling back to a smaller model like "google/flan-t5-small"
5. **Memory Limits**: If you get out-of-memory errors, adjust model parameters or choose a smaller model

## Updating Your Space

To make updates:
1. Edit files directly in the web interface, or
2. Push new changes using Git
3. Your Space will automatically rebuild with the new changes 