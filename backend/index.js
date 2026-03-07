import express from "express";
import Groq from "groq-sdk";
import dotenv from "dotenv";
import cors from "cors";

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const groq = new Groq({
  apiKey: process.env.GROQ_API_KEY
});

app.post("/chat", async (req, res) => {
  const userMessage = req.body.message;

  const response = await groq.chat.completions.create({
    messages: [{ role: "user", content: userMessage }],
    model: "llama-3.1-8b-instant"
  });

  res.json({
    reply: response.choices[0].message.content
  });
});

app.listen(3000, () => {
  console.log("AI server running on port 3000");
});