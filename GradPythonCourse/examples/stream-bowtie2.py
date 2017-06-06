import subprocess
import sys

path = sys.argv[1]  # path to unpaired FASTQ file
refpath = 'chr7'
outfile = path.replace('.fastq', '.sam')
handle = open(outfile, 'w')

p = subprocess.Popen(['bowtie2', '--quiet', '-x', refpath, '-U', path, '--local'], stdout=subprocess.PIPE)
for line in p.stdout:
    _, _, rname, _, mapq = line.split('\t')[:5]
    if line.startswith('@'):
        outfile.write(line)  # carry over header line
        continue
    if rname == 'chr7' and int(mapq) > 10:
        # only keep reads that mapped to chr7 with high quality
        outfile.write(line)

handle.close()
