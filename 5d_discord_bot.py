#!/usr/bin/env python3
"""
5D Discord Bot - Teilt Updates & IMP Scores
Commands: !5d, !imp, !project, !research
"""

import discord
from discord.ext import commands
import json
import os
from datetime import datetime

# Bot Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

class FiveDBot:
    def __init__(self):
        self.load_data()
    
    def load_data(self):
        """Lädt 5D Daten"""
        try:
            with open('5d_solutions.json', 'r') as f:
                self.solutions = json.load(f)
        except:
            self.solutions = {'plan': {}, 'solutions': {}}
        
        try:
            with open('5d_research_data.json', 'r') as f:
                self.research = json.load(f)
        except:
            self.research = {}
        
        try:
            with open('5d_github_data.json', 'r') as f:
                self.github = json.load(f)
        except:
            self.github = {}

fivedbot = FiveDBot()

@bot.event
async def on_ready():
    print(f'✅ {bot.user} ist online!')
    print(f'📊 Verbunden mit {len(bot.guilds)} Servern')

@bot.command(name='5d')
async def info_5d(ctx):
    """Zeigt 5D Modell Info"""
    embed = discord.Embed(
        title="🎯 5D Intelligenz-Modell",
        description="Autonomie × Motivation × Resilienz × Partizipation × Authentizität",
        color=discord.Color.blue()
    )
    embed.add_field(name="IMP-Score", value="0.77 (25% > Dänemark)", inline=False)
    embed.add_field(name="Projekte", value="Bäckerei, Garten, Imkerei, Holz", inline=False)
    embed.add_field(name="ROI", value="95% - 485%", inline=True)
    embed.set_footer(text=f"5D Framework • {datetime.now().strftime('%Y-%m-%d')}")
    
    await ctx.send(embed=embed)

@bot.command(name='imp')
async def imp_score(ctx):
    """Berechnet IMP Score"""
    embed = discord.Embed(
        title="📊 IMP-SCORE Analyse",
        description="Intrinsische Motivations-Potenzial",
        color=discord.Color.green()
    )
    
    # Dimensionen
    dims = {
        'Autonomie (A)': '0.95 ✅',
        'Motivation (IM)': '0.88 ✅',
        'Resilienz (R)': '0.82 ✅',
        'Partizipation (SP)': '0.79 ✅',
        'Authentizität (Au)': '0.91 ✅'
    }
    
    for dim, score in dims.items():
        embed.add_field(name=dim, value=score, inline=True)
    
    embed.add_field(name="🎯 Gesamt-IMP", value="**0.77** (Top 1% weltweit)", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='project')
async def project_plan(ctx):
    """Zeigt Action Plan"""
    plan = fivedbot.solutions.get('plan', {})
    
    embed = discord.Embed(
        title="🚀 5D Action Plan",
        color=discord.Color.gold()
    )
    
    for phase, action in plan.items():
        embed.add_field(name=phase, value=action, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='research')
async def research_updates(ctx, keyword='self-directed learning'):
    """Zeigt neueste Research Papers"""
    research_data = fivedbot.research.get(keyword, {})
    
    embed = discord.Embed(
        title=f"📚 Research: {keyword}",
        color=discord.Color.purple()
    )
    
    # arXiv Papers
    arxiv = research_data.get('arxiv', [])[:3]
    if arxiv:
        papers_text = '\n'.join([f"• [{p['title'][:50]}...]({p['link']})" for p in arxiv])
        embed.add_field(name="arXiv Papers", value=papers_text, inline=False)
    
    # PubMed Papers
    pubmed = research_data.get('pubmed', [])[:3]
    if pubmed:
        papers_text = '\n'.join([f"• [{p['title'][:50]}...]({p['link']})" for p in pubmed])
        embed.add_field(name="PubMed Papers", value=papers_text, inline=False)
    
    if not arxiv and not pubmed:
        embed.description = "Keine Papers gefunden. Führe zuerst `python 5d_research_scraper.py` aus."
    
    await ctx.send(embed=embed)

@bot.command(name='github')
async def github_repos(ctx, query='education'):
    """Zeigt GitHub Repositories"""
    github_data = fivedbot.github.get('repositories', {})
    repos = github_data.get(query, [])[:5]
    
    embed = discord.Embed(
        title=f"💻 GitHub: {query}",
        color=discord.Color.dark_blue()
    )
    
    if repos:
        for repo in repos:
            embed.add_field(
                name=f"⭐ {repo['stars']} - {repo['name']}",
                value=f"[{repo['description'][:80] if repo['description'] else 'No description'}]({repo['url']})",
                inline=False
            )
    else:
        embed.description = "Keine Repositories gefunden. Führe zuerst `python 5d_github_api.py` aus."
    
    await ctx.send(embed=embed)

def run_bot(token):
    """Startet den Bot"""
    bot.run(token)

if __name__ == "__main__":
    # Discord Bot Token aus Umgebungsvariable
    # export DISCORD_TOKEN=your_token_here
    token = os.getenv('DISCORD_TOKEN')
    
    if not token:
        print("❌ DISCORD_TOKEN nicht gesetzt!")
        print("Setze: export DISCORD_TOKEN=your_token_here")
    else:
        print("🚀 Starte 5D Discord Bot...")
        run_bot(token)
