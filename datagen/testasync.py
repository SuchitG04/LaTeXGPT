from prompts import *
from dotenv import load_dotenv
from together import AsyncTogether, Together
import asyncio
import time
import os
load_dotenv()

client = Together(
    api_key=os.getenv("TOGETHER_API_KEY"),
)

async_client = AsyncTogether(api_key=os.getenv("TOGETHER_API_KEY"))

t = ['\\begin{align*}+:\\bar{\\psi}(x)\\gamma _{\\mu }iS^{\\left( +\\right) }(x-y)\\gamma _{\\nu }\\psi\\end{align*}\n',
 '\\begin{align*}P\\bigl(S-E(S) \\ge v\\bigr) \\le \\exp\\Biggl(-\\frac{2v^{2}}{\\sum_{j=1}^{J}(b_{j}-a_{j})^{2}}\\Biggr).\\end{align*}\n',
 "\\begin{align*}~- \\partial_y (K(\\chi) \\partial_y \\chi) - \\frac{K'(\\chi)}{2} (\\partial_y \\chi)^2 + V'(\\chi) + v_i'(\\chi) \\delta(y - y_i) = \\sum_{n>0} \\frac{1}{M^n} \\frac{\\delta S^{(n)}_{h.d.}}{\\delta \\chi}.\\end{align*}\n",
 '\\begin{align*} \\rho\\,u^\\perp\\,=\\,\\nabla\\pi\\,,\\end{align*}\n',
 '\\begin{align*}\\eta(a_{l_n}p)=\\eta(a_{t_n-\\tau_n}p)>\\rho_0 e^{-\\gamma l_n}=\\rho_0 e^{-\\gamma(t_n-\\tau_n)}.\\end{align*}\n']


st = time.time()
res1 = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    messages=[
        {"role": "system", "content": description_sys_prompt},
        {"role": "user", "content": t[0]},
    ]
)
en = time.time()
print("Non Async: ", en-st)

async def gen():
    tasks = [
        async_client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            messages=[
                {"role": "system", "content": description_sys_prompt},
                {"role": "user", "content": msg},
            ]
        )
        for msg in t
    ]
    responses = await asyncio.gather(*tasks)
    return responses

st = time.time()
res = asyncio.run(gen())
en = time.time()

print("Non Async: ", en-st)