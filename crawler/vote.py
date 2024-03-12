import re
import plotly.graph_objects as go
from PttArticle import Article

class vote:
    def __init__(self, article: Article):
        self.article = article
        self.__vote_table = set()
        self.__vote_result = {}

        for push in reversed(article.push):
            match = re.search(r'@\d+', push)
            if match:
                netizen = push.split(':')[0][2:]
                self.__vote_table.add(netizen)
                key = match.group()  
                if key in self.__vote_result:
                    self.__vote_result[key] += 1
                else:
                    self.__vote_result[key] = 1
    
    @property
    def vote_result(self):
        return self.__vote_result

    def get_candiates_name(self, candidates):
        candidate_names = []
        for u in candidates:
            for line in self.article.content.split('\n'):
                if u in line:
                    candidate_name = line.split(' ')[0]
                    candidate_names.append(candidate_name)
        return candidate_names

    import plotly.graph_objects as go

    def vote_result_graph(self):
        _vote_result = sorted(self.__vote_result.items(), key=lambda x: int(x[0][1:]))
        candidates = [u[0] for u in _vote_result]
        candidates = self.get_candiates_name(candidates)
        votes = [u[1] for u in _vote_result]

        fig = go.Figure([go.Bar(x=candidates, y=votes, marker_color='#0080FF')])

        fig.update_layout(
            title=self.article.title,
            xaxis=dict(title='角色'),
            yaxis=dict(title='得票數')
        )

        fig.show()


        

if __name__ == '__main__':
    article = Article('https://www.ptt.cc/bbs/C_Chat/M.1710226285.A.19E.html')
    v = vote(article)
    v.vote_result_graph()
