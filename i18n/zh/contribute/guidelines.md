# Tutorial styling guidelines

So you've decided to write a tutorial for TON Documentation?

We're excited to have you among our contributors! Please review the guidelines below to make sure your tutorial follows the style and quality of the pre-existing content on TON Docs.

It is important that you take some time to become familiar with the tutorial structure and how headings should be used. Please read through some of our pre-existing tutorials and also have a look at [previous Pull Requests](https://github.com/ton-community/ton-docs/pulls?q=is%3Apr+is%3Aclosed) before submitting your own.

## Process

:::info IMPORTANT
Before you start writing, *read the guidelines below*! They will help you ensure the level of standardization and quality that will make the review process much faster.
:::

Also, be sure to refer to the [**sample tutorial structure**](/contribute/sample-tutorial) we have provided.


1. To begin, fork and then clone the [ton-docs](https://github.com/ton-community/ton-docs/) repository on GitHub and create a new branch in your local repository.
2. Write your tutorial keeping quality and readability in mind! Have a look at the existing tutorials to see what you should aim for.
3. When you're ready to submit it for review, [open a Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) from your branch. We will be notified, and the review process will begin:
    1. **Please make every effort to submit only the final draft of your tutorial**. Some typos and grammar fixes are acceptable, but if there are significant changes to be made before we can publish the tutorial, it will take much longer to review and have you make the necessary changes.
4. Once we've reviewed your submission and you've made all necessary changes, we'll merge the Pull Request and publish the tutorial on TON Documentation. We'll contact you shortly after this to arrange your payment!
5. Once it is published, remember to **promote** your tutorial on social media! The [documentation maintainers](/contribute/maintainers) can help to amplify this promotion as long as you cooperate with us.

To summarize, the workflow is as follows:  
1. ***Fork and Clone*** the **`ton-docs`** repository
2. ***Write and polish*** your tutorial
3. ***Submit a Pull Request*** for review
4. ***Make any necessary changes***
5. The tutorial is ***merged and published***
6. ***Promote your tutorial*** on social media!

## General tips

- **Do not copy and paste pre-existing content**. Plagiarism is a serious issue and will not be tolerated. If the tutorial is inspired by some existing content, reference it and link to it. When linking to other tutorials/resources, use TON Docs resources if possible.
- **Include any walkthrough videos or video content** in the PR by uploading it to Google Drive.
- **Account funding from faucets must be clearly explained**, including which account is being funded, from where, and why. Do not assume learners can accomplish this task on their own!
- **Display sample outputs** in the form of Terminal snippets or screenshots to help learners understand what to expect. Trim long outputs.
- **Take an error-driven approach** where you bump into errors on purpose to teach learners how to debug them. For example, if you need to fund an account to be able to deploy a contract, first try and deploy without funding, observe the error that is returned, then fix the error (by funding the account) and try again.
- **Add potential errors and troubleshooting.** Of course, the tutorial shouldn't list every possible error, but it should make an effort to catch the important or most common ones.
- **Use React or Vue** for the client-side.
- **Before making the PR, run the code by yourself first** to avoid any obvious errors and make sure it works as expected.
- **Avoid including external/cross-links** to different sources between tutorials. If your tutorial is longer, we can discuss how to turn it into a longer course or Pathway.
- **Provide** **pictures or screenshots** to illustrate the complicated processes where needed.
- Upload your images to the `static` directory of the learn-tutorials repository — **DO NOT** use hotlinks to external sites, as this can result in broken images.
- **Image links must** **be in markdown format** and you must **ONLY** use the raw GitHub URL of the static directory in the repository: `![name of your image](https://raw.githubusercontent.com/ton-community/ton-docs/main/static/img/tutorials/<your image filename>.png?raw=true)`
    - Remember to add `?raw=true` at the end of the URL.

## How to structure your tutorial

:::info Sample tutorial structure
Feel free to check out the [sample tutorial structure](/contribute/sample-tutorial) to see it with your own eyes.
:::

- The **Title** should be direct and clear, summarizing the tutorial's goal. Do not add the tutorial title as a heading inside the document; instead, use the markdown document filename. 
  - *For example*: If your tutorial was titled "_Step by step guide for writing your first smart contract in FunC_," the filename should be:  
  `step-by-step-guide-for-writing-your-first-smart-contract-in-func.md`
- Include an **Introduction** section explaining *why* this tutorial matters and what the context of the tutorial is. Don't assume that it is obvious.
- Include a **Prerequisites** section explaining any *prior knowledge* required or any existing tutorials that need to be completed first, any tokens that are needed, etc.
- Include a **Requirements** section explaining any *technologies that must be installed* **prior** to starting the tutorial and that the tutorial will not cover, such as the TON Wallet extension, Node.js, etc. Do not list packages that will be installed during the tutorial.
- Use **subheadings** (H2: ##) to break down your explanations within the body of the tutorial. Keep the Table of Contents in mind when using subheadings, and try to keep them on point.
    - If the content below a subheading is short (for example, only a single paragraph and a code block), consider using bold text instead of a subheading.
- Include a **Conclusion** section that summarizes what was learned, reinforces key points, and also congratulates the learner for completing the tutorial.
- (***Optional***) Include a **What's Next** section pointing to good follow-up tutorials or other resources (projects, articles, etc.).
- (***Optional***) Include an **About The** **Author** section at the end. Your bio should include a link to your GitHub profile (which will have your name, website, etc.) and a link to your Telegram profile (so that users can contact/tag you for help and questions).
- A **References** section **must** be present if you have taken any help in writing this tutorial from other documents, GitHub repos, or other tutorials. Credit sources by adding their name and a link to the document when possible (if it is not a digital document, include an ISBN or other means of reference).

## Style Guide

- **Writing Tone -** Tutorials are written by community contributors for their peers. 
  - Given this, we recommend creating a tone of inclusion and interaction throughout the tutorial. Use words such as “we”, “us”, “our”.
    - _For example_: "We have successfully deployed our contract."
  - When providing direct instructions, feel free to use “you”, “your”, etc.
    - _For example_: “*Your file should look like this:*”.
- **Use Markdown properly** throughout your tutorial. Refer to [GitHub's markdown guide](https://guides.github.com/features/mastering-markdown/) as well as the [sample tutorial structure](/contribute/sample-tutorial).
- **Do not use pre-formatted text for emphasis**, *for example*:
    - ❌ "TON counter `smart contract` named `counter.fc`" is incorrect.
    - ✅ "TON counter **smart contract** named `counter.fc`" is correct.
- **Do not use any markdown formatting in a section heading**, *for example*:
    - ❌ # **Introduction** is incorrect.
    - ✅ # Introduction is correct.
- **Explain your code!** Don't just ask learners to blindly copy and paste.
    - Function names, variables, and constants **must** be consistent across the entire document.
    - Use a comment at the beginning of a code block to show the path and filename where the code exists. *For example*:

        ```jsx
        // test-application/src/filename.jsx
        
        import { useEffect, useState } from 'react';
        
        ...
        ```

- **Select the appropriate language** for code block syntax highlighting!
    - All code blocks *must* have syntax highlighting. Use **```text** if you are not sure what kind of syntax highlighting to apply.
- **Do not use code block syntax for pre-formatted text,** *for example*:
    - ❌ \```filename.jsx\``` is incorrect.
    - ✅ \`filename.jsx\` is correct.
- **Your code blocks should be well commented**. Comments should be short (usually two or three lines at a time) and effective. If you need more space to explain a piece of code, do it outside of the code block.
- **Remember to leave a blank line** before and after all code blocks.  
  *For example*:

```jsx  
  
// test-application/src/filename.jsx  
  
import { useEffect, useState } from 'react';
  
```  

  
- **Use a linter & prettifier** before pasting your code into the code blocks. We recommend `eslint` for JavaScript/React. Use `prettier` for code formatting.
- **Avoid the overuse of bullet points**, numbered lists, or complicated text formatting. The use of **bold** or *italic* emphasis is allowed but should be kept to a minimum.

# **App setup**

- Web3 projects will typically include several existing code libraries. Be sure to account for this when writing your tutorial. Where possible, provide a GitHub repository as a starting point to make it easier for learners to get started.
- If you are *not* using a GitHub repo to contain the code used in your tutorial, remember to explain to readers how to create a folder to keep the code organized. 
*For example*: `mkdir example && cd example`
- If you use `npm init` to initialize a project directory, explain the prompts or use the `-y` flag.
- If you use `npm install` use the `-save` flag.
