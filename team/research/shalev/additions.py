import re,sys
p='docs/books/the-art-of-ai-monks-en.md'
t=open(p).read()
def ins_before(anchor, block):
    global t
    assert t.count(anchor)==1, anchor
    t=t.replace(anchor, block.strip('\n')+'\n\n'+anchor)

CH3 = '''
### The creator's pre-history, in his own posts

A history without a "first" still has people in it. Read back on 23 October 2026, Shalev Hani's public X timeline shows that the robe was not his first experiment. In December 2023 he posted a breakdown of taking a POV app's TikTok and Instagram accounts to tens of millions of views in 60 days, with a rule he would repeat for years: most new videos should be remakes of earlier winners with a changed hook. [S44]

In March 2024 he described five months of AI-made TikTok Shop videos, more than 20 million views and "five figures in profit". Two months later he advised beginners to put "may," "might," and "potentially" in front of any claim. [S44], [S45] In April 2026 he summarized his own background as an early student of the Creators Corner program from July 2023, work with more than 100 brands, and more than 3,000 AI videos before Yang Mun. [S37] These are self-descriptions, not audited résumés. They matter because they turn the story from a lucky afternoon into what he calls "year 3": a person who spent years learning short-form scripts and commerce before giving them a monk's face.

That framing also corrects a common misreading of the category. The monk was a new costume on an older craft: rewriting proven hooks, matching visuals to a script, and connecting attention to a product.
'''
ins_before('## Chapter 4. Yang Mun and Shalev Hani', CH3)

anchor='These figures use different periods, categories, and evidence. Revenue is money'
UPD = '''
Update, 23 October 2026. The pinned post behind that headline was read back through X's public API. It is a long-form X article dated 9 April 2026, titled "I Built a Fake AI Monk, Made $500K in 6 Months. Now Everyone's Copying It. (Full Guide)." In it, Hani writes that Yang Mun made him $300,000 and gained 5 million followers in three months, reached $500,000 in six months, and that "the $500K" came "100% [from] digital products." He also says he now runs seven characters on the same system. [S31] Reading the body authenticates what the creator wrote and when; it does not audit the figures. His own later posts describe the result variously as "$500K PROFIT," "$467K in 7 months," and "$300k Profit (90 Days)," so the revenue-versus-profit question below remains open. [S33], [S46], [S47]
'''
ins_before(anchor, UPD)

CH4 = '''
### The creator's own chronology

Hani has published a long trail of posts and X articles about Yang Mun. Read together on 23 October 2026, they give a dated sequence in his own words. Each line below is his claim, with the date of the post. [S33]–[S43]

- **2023–2025.** AI content for brands and TikTok Shop, a POV-app growth case, and, by his account, three years of short-form work before the monk. [S37], [S44]
- **23 January 2026.** "Everyone is copying this AI character... I'm the one behind it," with 400 million-plus organic views, "$300k Profit (90 Days)," and 5 million followers. [S33]
- **3 February 2026.** A tool breakdown: a locked character image, a custom deep voice slowed by about 10 percent "because wisdom sounds better when it's slow," and a lip-sync step, followed by the line "Tools create content. Systems create cash." [S34]
- **12 February 2026.** He says he declined a $325,000 cash offer for Yang Mun at nearly 6 million followers. Columbia News Service later reported the same rejected figure. [S35], [S02]
- **9 April 2026.** The pinned "Full Guide" article: a five-step system of distinctive character, empathy-and-solution scripts, one fixed voice, three posts a day per platform, and digital products only. [S31]
- **14 April 2026.** "I Tested 200+ AI Scripts": three formulas he credits with about 70 million views. [S36]
- **16–28 July 2026.** He announces that he sold Yang Mun for $170,000 and explains what he believes the buyer bought. [S38], [S39]

The sequence is useful precisely because it is first-person. It shows how the creator explains his own work, which claims he repeats, and how the story changes as the business changes. It is not a substitute for the independent reporting cited above, and nothing in it resolves the identity statement in [S03].

### The sale: what the creator says was bought

On 16 July 2026 Hani posted that he had sold "a fake AI monk for $170,000," listing 6 million followers, 22,000 buyers on an email list, and a 5,000-person community. [S38] In a longer article twelve days later he argued that the followers were "the least valuable thing in the whole deal": "The followers were the billboard. The 22,000 buyers and the 5,000 members were the business." He describes pricing the character "like any business: on the revenue it produces," as a multiple of reliable monthly income, and says he kept "the one thing that actually mattered: knowing how to build the next one." [S39]

We could not verify the buyer, contract, or payment, and the sale explains why the present operator of the Yang Mun accounts may differ from the creator named in [S01] and [S02]. Readers should treat later Yang Mun content as possibly made under new ownership. The sale price is also lower than the $325,000 offer he says he refused in February. [S35] The record does not explain the gap, and we do not guess.

The durable lesson is the one he states himself, and it matches this book's argument from the other direction. Attention is rented. An owned relationship with people who have chosen to buy something useful is the asset. A character is the front door.
'''
ins_before('### What a creator can actually take away', CH4)

CH5 = '''
### Three formulas the creator published

Hani's April 2026 article names three script structures he says outperformed more than 200 others. [S36] They are worth studying as structures, with one caveat each.

1. **The reframe.** Do not tell viewers to stop a habit they feel guilty about. Redirect it: "If you're going to overthink… then overthink the positive." He reports 24 million views for that line. The viewer is understood rather than attacked.
2. **"You're doing it wrong."** Take an ordinary daily act and say it has been done wrong, then list fixes. His example is drinking water; he reports 23 million views. This is the formula most likely to slide into unsupported health claims. Use it for harmless tasks, such as packing a bag or starting an email, and keep any health statement within what a qualified source supports. See Chapter 9.
3. **Validation.** Teach nothing new. Say clearly what the audience already feels: "Keep it private until it's permanent." He reports 22.4 million views. "You're not the teacher here. You're the mirror."

His pinned guide adds a timing skeleton: about two seconds to show understanding without judgment, three seconds to flip or promise a specific fix, twenty to forty seconds to teach one usable thing, and three seconds to connect it to who the viewer wants to become. [S31] The view counts are his. The skeleton is consistent with the one-message structure observed in Chapter 4, and it is a reasonable starting brief for an original character.
'''
ins_before('## Chapter 6. From Scroll to Store', CH5)

CH6 = '''
### The creator's staircase of offers, and where it needs brakes

In his pinned guide Hani describes Yang Mun as selling "digital products only," with "no affiliate deals." [S31] By June 2026 he was describing a broader staircase across his characters: ebooks around $15–$25, supplement affiliate links, a $10–$20 monthly community, a $4,000 high-ticket offer delivered with a hired certified professional, and finally selling the account. He says he had sold two smaller accounts for $8,000 and $11,000 at that point. [S40]

Two parts of that staircase deserve brakes. A character who gives health advice and also earns commission on supplements creates a conflict that viewers cannot see unless it is disclosed plainly, and Chapter 9's claim review applies with full force. A high-ticket offer sold by a synthetic face must make clear, before payment, which real, qualified human delivers the service. Hani's own example puts a certified professional in that role. [S40] The structure he describes, a free daily message, an inexpensive first product, and a deeper paid relationship, is the same one this book recommends. The difference is in the quality and honesty of each step.
'''
ins_before('## Chapter 7. The Content Factory', CH6)

CH9 = '''
### What the creator says about disclosure and care

The creator's posts show several positions that are hard to reconcile. In January 2026 he wrote that a new character "clearly labeled as AI in the bio" still made sales, adding that "people are impulsive they don't read." [S41] In May he wrote that his AI monk "has helped more people with their mental health than most real therapists on Instagram... He's not real. But the messages I get from his followers are." [S43] In the same month he warned that waves of account bans were driven less by AI detection than by incentivized "comment YES" calls to action. [S42]

Each statement points to an obligation. A label in a bio that he expects buyers not to read is not meaningful disclosure; disclosure has to appear where the decision is made, in the video, the caption, and the checkout. Messages from people in distress are a responsibility, not a metric; a character that receives them needs a human escalation path and crisis resources, and must never present itself as therapy. Platform rules about engagement bait are part of the ethics too, because a banned account strands the people who trusted it.

The broader question of "fake people" is not whether a character may be fictional. Fiction, parable, and the teaching persona are old. It is whether the audience can understand what is speaking to them, whether the advice survives a qualified review, and whether a vulnerable viewer is treated as a person rather than a conversion.
'''
ins_before('## Chapter 10. Build a Different Character', CH9)

APPB = '''
A follow-up pass on 23 October 2026 read back Shalev Hani's public X timeline, original posts and long-form X articles from December 2023 to October 2026 (about 250 posts), through X's public API. Fifteen dated items are cited as S31 and S33–S47. They are first-person creator statements. They establish what he published and when, not audited revenue, profit, ownership, or the terms of any sale. Retweets, replies, images, and video were not reviewed. A running research log is kept with the companion materials so later passes can extend the record.
'''
ins_before('## Appendix C. References', APPB)

old31 = re.search(r'^\*\*S31\. .*$', t, re.M).group(0)
t = t.replace(old31, '**S31. Shalev Hani, pinned X article, "I Built a Fake AI Monk, Made $500K in 6 Months. Now Everyone\'s Copying It. (Full Guide)."** Published 9 April 2026; first found 22 October 2026, body read back through the X API on 23 October. Creator account of origin, five-step system, script timing and revenue claims; not an audit. [Source][S31]')

REFS = [
 ('S33','2014732472664076414','X post, "Everyone is copying this AI character."','23 January 2026','Creator claims of 400M+ views, $300k profit in 90 days, 5M followers.'),
 ('S34','2018725900959822131','X article, "The exact blueprint I used to build \'Yang Mun\' into a $300k profit machine."','3 February 2026','Creator tool and voice workflow; links to his paid blueprint.'),
 ('S35','2021989884882244010','X post on declining a $325,000 offer.','12 February 2026','Creator statement; matches the figure reported in S02.'),
 ('S36','2044099931494068455','X article, "I Tested 200+ AI Scripts. These 3 Formulas Got 70 Million Views."','14 April 2026','Creator-reported view counts for three script formulas.'),
 ('S37','2049166336002343021','X post on his background before Yang Mun.','28 April 2026','Self-described training, brand work and video count.'),
 ('S38','2077788420240494866','X post, "I just sold a fake AI monk for $170,000."','16 July 2026','Creator sale announcement; buyer, contract and payment unverified.'),
 ('S39','2082119075095060964','X article, "How I Built a Fake AI Monk Into a $170K Exit (Full Breakdown)."','28 July 2026','Creator explanation of what the buyer acquired and how he priced it.'),
 ('S40','2070484602112901418','X article, "How ONE AI Character Makes Money 5 Ways."','26 June 2026','Creator description of offer tiers across his characters and two smaller account sales.'),
 ('S41','2012564307071127718','X post on sales from a character labeled as AI.','17 January 2026','Creator claim; sales figure unverified.'),
 ('S42','2052265003051524464','X post on account bans and incentivized calls to action.','7 May 2026','Creator interpretation of platform enforcement.'),
 ('S43','2056389501816303742','X post on followers\' mental-health messages.','18 May 2026','Creator statement; messages not reviewed.'),
 ('S44','1765717627110895699','X thread on AI TikTok Shop content.','7 March 2024','Earlier creator claim of 20M+ views and five-figure profit; see also his December 2023 POV-app thread.'),
 ('S45','1785762655623434673','X thread item on cautious claim wording.','1 May 2024','Creator advice to qualify claims with "may," "might," "potentially."'),
 ('S46','2056718288823198031','X post summarizing seven characters and "$500k PROFIT."','19 May 2026','Creator claim using "profit"; compare S31 and S47.'),
 ('S47','2052024190547710355','X article, "AI Monk + Claude = $467K in 7 months."','6 May 2026','Creator title figure differing from S31 and S46.'),
]
sec = '### Creator\'s own posts, read back 23 October 2026\n\n' + '\n\n'.join(f'**{r}. Shalev Hani, {title}** Published {date}; read back 23 October 2026. {note} [Source][{r}]' for r,i,title,date,note in REFS) + '\n\n'
first_def = '[S01]: https://www.heygen.com/customer-stories/yangmun'
ins_before(first_def, sec)
t = t.rstrip('\n') + '\n' + '\n'.join(f'[{r}]: https://x.com/shalevhvs/status/{i}' for r,i,*_ in REFS) + '\n'
open(p,'w').write(t)
print('ok')
