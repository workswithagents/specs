import { AssistantAgent, UserProxyAgent, GroupChat } from "autogen";

const codeAgent = new AssistantAgent({
  name: "CodeAgent",
  systemMessage: "You write and review TypeScript code.",
});

const user = new UserProxyAgent({
  name: "User",
  humanInputMode: "NEVER",
  codeExecution: false,
});

const chat = new GroupChat([codeAgent, user]);
const result = await chat.run("Write a function to validate email addresses");
console.log(result.summary);
