from __future__ import print_function
import sys, os
import subprocess
import optparse
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def get_SRR_list(ID):
    headers = {'User-Agent': 'Mozilla/5.0'}
    DB='https://www.ncbi.nlm.nih.gov/sra/?term='+ID

    req=Request(DB,headers=headers)
    webpage=urlopen(req)
    soup=BeautifulSoup(webpage,"html.parser")
    table = soup.find_all('table')
    data =[]
    for t in table:
        for tr in t.find_all('tr'):
            tds = list(tr.find_all('td'))
            for td in tds:
                if td.find('a'):
                    srr_id = td.find('a').text
                    if srr_id.startswith('SRR'):
                        data.append(srr_id) 
    return data

def run_prefetch(prefetch,ID,outD):
    cmd=[prefetch,ID,"-o",outD+'/'+ID+'.sra']
    proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    return stdout.decode('utf-8').rstrip('\n'),stderr.decode('utf-8').rstrip('\n')

def main(ncbi_table,library_type,prefetch,outD):
    except_sra=[i.split('.sra')[0] for i in os.listdir(outD) if i.endswith('sra')] # check output folder

    from_ncbi=[] # sample accession info from ncbi
    with open(ncbi_table,'r') as N:
        for i in N:
            i=i.rstrip('\n')
            if i.startswith('#') or not i:
                continue
            from_ncbi.append([i.replace('"','') for i in i.split('","')])
    df_n=pd.DataFrame(from_ncbi[1:],columns=from_ncbi[0])

    sample_acc=set(df_n[(~df_n['Sample Accession'].isin(except_sra)) & (df_n['Library Strategy']==library_type)]['Sample Accession'])

    for i in sample_acc: #run prefetch
        out,err=run_prefetch(prefetch,i,outD)
        if out:
            print (out)
        if err:
            print("WARNING: ", err,"\nParsing ncbi sra\n", file=sys.stderr)
            acc_tmp=get_SRR_list(i) #parsing SRR accession number again
            for a in acc_tmp:
                out2,err2=run_prefetch(prefetch,a,outD)
                if err2:
                    print("WARNING: ", err2, file=sys.stderr)
                if out2:
                    print (out2)

if __name__=="__main__":
    usage = "get SRA file from NCBI sample accession"
    parser = optparse.OptionParser(usage)
    parser.add_option("-i","--input",dest="ncbi_table",
            help="ncbi_table from BIOPROJECT",type="string")
    parser.add_option("-l","--library_type",dest="library_t",
            help="WGS or AMPLICON",type="string")
    parser.add_option("-o","--output",dest="outputf",
            help="sra download folder",type="string")
    parser.add_option("-p","--prefetch",dest="prefetch",
            help="sra prefetch path from sra tools",type="string") 
    (opts,args)=parser.parse_args()

    if opts.ncbi_table is None or opts.library_t is None or opts.outputf is None or if opts.prefetch is None:
        parser.print_help()
    else:
        main(opts.ncbi_table,opts.library_t,opts.prefetch,opts.outputf)
