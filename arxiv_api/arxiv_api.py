import urllib
import os,sys
import pickle
sys.path.append('feedparser-5.2.1/feedparser')
import feedparser

arxiv_content=[]

feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

rss_collections = ['hep-ex','hep-ph']
listed_arxiv = []
counter = 1

updated = ''

for rss in rss_collections:
    
    response = urllib.urlopen('http://export.arxiv.org/rss/'+rss).read()

    feed = feedparser.parse(response)

    if counter == 1:
      # print out feed information
      # print 'Feed title: %s' % feed.feed.title
      updated = feed.feed.updated.split('T')[0]
      # print 'Feed last updated: %s' % feed.feed.updated
      print 'Feed last updated: %s' % updated
      # print 'totalResults for this query: %s' % feed.feed.opensearch_totalresults
      arxiv_content.append("{Date: "+updated+"}\\\\")

    arxiv_content.append("{\\color{red} \\bf Listing "+rss+"}\\\\")
    arxiv_content.append("\\vspace{2mm}")
    
    for entry in feed.entries:
        arxiv_id = entry.id.split('/abs/')[-1]
        arxiv_id_title = entry.title.split("(arXiv",1)[0].replace("&","and").replace("\\","").replace("_","\\_")
        arxiv_id_ver = entry.title.split("(arXiv",1)[1].split(' [')[0].split('v')[1].encode("utf-8")
        if arxiv_id in listed_arxiv: continue
        else: listed_arxiv.append(arxiv_id)
        arxiv_content.append("{\\color{red} "+str(counter)+")} {\\color{blue} \\small \href{http://arxiv.org/abs/"+arxiv_id+"}{"+arxiv_id_title+"}}")
        arxiv_content.append(arxiv_id+" (v"+arxiv_id_ver+")")
        authors = entry.author.split('">')
        authors = [i.split(',', 1) for i in authors]
        authors = [j for i in authors for j in i][1::2]
        authors = [i.split('<', 1)[0].encode("utf-8").replace("&","").replace("#","") for i in authors]
        authors = filter(lambda name: name.strip(),authors)
        authors = ", ".join(authors)
        arxiv_content.append("\\\\")
        arxiv_content.append("{\\tiny "+authors+"}")
        # arxiv_content.append("{\small "+entry.author.name+"}")
        # arxiv_content.append("{\small ".join(author.name for author in entry.authors)+"}")
        # arxiv_content.append("\\\\")
        arxiv_content.append("\\vspace{1mm}")
        arxiv_content.append("\n")
        # sys.exit(1)
        counter = counter +1

# sys.exit(1)

##########################################################################################
##########################################################################################

class cfile(file):
    #subclass file to have a more convienient use of writeline
    def __init__(self, name, mode = 'r'):
        self = file.__init__(self, name, mode)

    def wl(self, string):
        self.writelines(string + '\n')
        return None
    
with open("template.tex") as f:
  template_content = [x.strip('\r') for x in f.readlines()]
  template_content = template_content+arxiv_content
  template_content.append('\n\end{document}\n')

fid = cfile(updated+'.tex', 'w')
for line in template_content:
  fid.wl(line)
  # print line
fid.close()

# os.system("pdflatex -jobname="+str(sys.argv[1])+" -interaction nonstopmode -halt-on-error -file-line-error template2.tex \
os.system("pdflatex -interaction nonstopmode -halt-on-error -file-line-error "+updated+".tex \
                                                                                                                      | tail \
                                                                                                                          ")
                                                                                                                           # > /dev/null \
os.system("rm *.log *.aux *.out")
