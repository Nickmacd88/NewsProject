from sentence_transformers import SentenceTransformer, util
import sqlite3
import numpy as np
import torch

class Base_Article_Comparator:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2", cache_folder="./cache")

    """Compares two articles and returns a similarity score"""
    def compare(self, article):
           pass
    """Creates an embedding of an article"""
    def embed(self, article:str):
        pass

    def _connect(self):
        self.con = sqlite3.connect('../data/news.db')


class Article_Comparator(Base_Article_Comparator):
    def __init__(self):
        super().__init__()

    def compare(self, article1, article2):
        embedding1 = self.model.encode(article1, normalize_embeddings=True)
        embedding2 = self.model.encode(article2, normalize_embeddings=True)

        return util.cos_sim(embedding1, embedding2)

    def _load_embeddings(self):
        self._connect()
        cur = self.con.cursor()
        cur.execute("SELECT * FROM news_articles")
        rows = cur.fetchall()
        # Now I need to iterate through, build
        articles = []
        embeddings = []
        for row in rows:
            id, title, url, text, date, authors, embedding = row
            articles.append([id, title, url, text, date, authors])
            vec = np.frombuffer(embedding, dtype=np.float32)
            embeddings.append(torch.tensor(vec))
        embeddings = torch.stack(embeddings)
        return articles, embeddings



    def top_k(self, article, k=3):
        articles, embeddings = self._load_embeddings()
        q_embeddings = self.model.encode(article, normalize_embeddings=True)
        scores = util.cos_sim(q_embeddings, embeddings)
        results = []
        topk = torch.topk(scores, min(k, len(scores[-1])))
        for score, idx in zip(topk.values[-1], topk.indices[-1]):
            print("Score: {score}\nindex: {idx}".format(score=score, idx=idx))
            results.append({
                "title": articles[idx][1],
                "url": articles[idx][2],
                "text": articles[idx][3],
                "score": float(score)
            })
            print(results)
        return results

if __name__ == "__main__":
    comparator = Article_Comparator()
    article = "The Justice Department on Friday released the long-awaited transcripts of a weeks-old interview it conducted with convicted Jeffrey Epstein associate Ghislaine Maxwell.The Maxwell interview was one of two steps the White House took to try and quell outrage over its handling of the Epstein files, which has rocked the administration for weeks and caused even many supporters of President Donald Trump to balk.Attorney General Pam Bondi and other officials had built up anticipation for the Epstein documents before pulling back on promises to release them. Trump has also made a series of false and misleading claims that have caused Epstein’s victims to suggest a cover-up.The administration’s other big move – asking to unseal grand jury testimony – hasn’t amounted to much. In fact, two judges have suggested it was a “diversion” intended to look transparent without actually being so.The Maxwell interview conducted by Deputy Attorney General Todd Blanche, likewise, doesn’t add much to the public knowledge of Epstein. But there are some key points worth running through – particularly in the broader context of the administration’s botched handling of the matter.Here’s what to know from the transcript:Maxwell isn’t coming clean, which undercut the exercise The Maxwell interview is the administration’s first significant release of information since its effort to close the matter blew up in its face last month. (Also on Friday, it sent Epstein documents to a House committee that had demanded them, but those aren’t public yet.) But it was always a weird choice, given Maxwell is a convicted sex offender and her appeals are ongoing. The Justice Department in Trump’s first term also labeled her a brazen liar. What could she possibly add of value? Not a whole lot, it seems. The big headlines are that Maxwell doesn’t implicate anybody – including Trump – in any wrongdoing and says Epstein didn’t have a client list. But those statements might carry more weight if Maxwell came clean about her and Epstein’s own misdeeds. She clearly didn’t do that. In fact, she repeatedly cast doubt on them, too. She denied that Epstein paid her millions of dollars to recruit young women for him. She denied witnessing any nonconsensual sex acts. And she denied seeing anything “inappropriate” from “any man” – seemingly including Epstein. “I never, ever saw any man doing something inappropriate with a woman of any age,” Maxwell said. “I never saw inappropriate habits.” Some other Maxwell responses also call her credibility into question. In another instance, Maxwell claimed Epstein didn’t have “inappropriate” cameras inside his New York, Caribbean, New Mexico and Paris residences. Cameras in his Palm Beach, Florida, house were used because money was being stolen. But Epstein’s seven-story townhouse in Manhattan was outfitted with cameras, the New York Times reported earlier this month. Several of Epstein’s victims have cited a network of hidden cameras. In another instance, Maxwell indicated she didn’t recall recruiting a masseuse from Trump’s Mar-a-Lago resort – seemingly denying Virginia Giuffre’s claim that that’s where Maxwell recruited her. “I’ve never recruited a masseuse from Mar-a-Lago for that, as far as I remember,” she said. But the next day, Maxwell made a point to water down that denial. “I don’t remember anybody that I would have [recruited],” Maxwell said. “But it’s not impossible that I might have asked someone from there.”"
    results =  comparator.top_k(article)
    for article in results:
        print(article['title'])
