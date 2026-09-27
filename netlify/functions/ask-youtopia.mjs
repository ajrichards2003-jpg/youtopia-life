import OpenAI from "openai";
import { getUser } from "@netlify/identity";
const DAILY_LIMIT=5;
const buckets=new Map();
export default async (req, context) => {
  if(req.method!=="POST") return new Response(JSON.stringify({error:"Method not allowed"}),{status:405,headers:{"content-type":"application/json"}});
  const user=await getUser();
  if(!user?.email) return new Response(JSON.stringify({error:"Please sign in to Ask Youtopia."}),{status:401,headers:{"content-type":"application/json"}});
  const body=await req.json().catch(()=>({})); const question=String(body.question||"").trim().slice(0,600);
  if(!question) return new Response(JSON.stringify({error:"Ask a question first."}),{status:400,headers:{"content-type":"application/json"}});
  const day=new Date().toISOString().slice(0,10), key=user.email+"|"+day, used=buckets.get(key)||0;
  if(used>=DAILY_LIMIT) return new Response(JSON.stringify({error:"You've used today's 5 launch questions. Come back tomorrow."}),{status:429,headers:{"content-type":"application/json"}});
  const client=new OpenAI();
  const response=await client.responses.create({model:"gpt-5.6-luna",input:[
    {role:"system",content:"You are Ask Youtopia, the evidence-aware discovery guide for Youtopia Life. Be concise, curious and useful. Distinguish established evidence, promising evidence, emerging research, anecdote and unresolved claims. Never treat a product claim as proof. Do not diagnose or prescribe. When relevant suggest what primary-source evidence the user should inspect and note uncertainty. Youtopia philosophy: curious enough to investigate, rigorous enough to question, independent enough to change our minds."},
    {role:"user",content:question}
  ],max_output_tokens:500});
  const answer=response.output_text||"I couldn't produce an answer this time.";
  buckets.set(key,used+1);
  return new Response(JSON.stringify({answer,remaining:DAILY_LIMIT-used-1}),{headers:{"content-type":"application/json"}});
};