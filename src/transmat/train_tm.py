import sys
import getopt
import logging
import numpy as np
from space import Space
from utils import read_dict, train_tm

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('align')


def train_translation_matrix(source_file, target_file, dict_file, out_file):
    """Trains a transltion matrix between the source and target languages, using the words in dict_file as anchor
    points and writing the translation matrix to out_file

    Note that the source language file and target language file must be in the word2vec C ASCII format

    :param source_file: The name of the source language file
    :param target_file: The name of the target language file
    :param dict_file: The name of the file with the bilingual dictionary
    :param out_file: The name of the file to write the translation matrix to
    """
    log.info("Reading the training data")
    train_data = read_dict(dict_file)

    #we only need to load the vectors for the words in the training data
    #semantic spaces contain additional words
    source_words, target_words = zip(*train_data)

    log.info("Reading: %s" % source_file)
    source_sp = Space.build(source_file, set(source_words))
    source_sp.normalize()

    log.info("Reading: %s" % target_file)
    target_sp = Space.build(target_file, set(target_words))
    target_sp.normalize()

    log.debug('Words in the source space: %s' % source_sp.row2id)
    log.debug('Words in the target space: %s' % target_sp.row2id)

    log.info("Learning the translation matrix")
    log.info("Training data: %s" % str(train_data))
    tm = train_tm(source_sp, target_sp, train_data)

    log.info("Printing the translation matrix")
    np.savetxt(out_file, tm)

def usage(errno=0):
    print >>sys.stderr,\
    """
    Given train data (pairs of words and their translation), source language and 
    target language vectors, it outputs a translation matrix between source and 
    target spaces.

    Usage:
    python train_tm.py [options] train_data source_vecs target_vecs 
    \n\
    Options:
    -o --output <file>: output file prefix. Optional. Default is ./tm
    -h --help : help

    Arguments:
    train_data: <file>, train dictionary, list of word pairs (space separated words, 
            one word pair per line)
    source_vecs: <file>, vectors in source language. Space-separated, with string 
                identifier as first column (dim+1 columns, where dim is the dimensionality
                of the space)
    target_vecs: <file>, vectors in target language


    Example:
    python train_tm.py train_data.txt ENspace.pkl ITspace.pkl

    """
    sys.exit(errno)


def main(sys_argv):

    try:
        opts, argv = getopt.getopt(sys_argv[1:], "ho:",
                                   ["help", "output="])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(1)

    out_file = "./tm"
    for opt, val in opts:
        if opt in ("-o", "--output"):
            out_file = val
        elif opt in ("-h", "--help"):
            usage(0)
        else:
            usage(1)

    if len(argv) == 3:
        source_file = argv[1]	
        target_file = argv[2]
	dict_file = argv[0]
    else:
	print str(err)
	usage(1)

    train_translation_matrix(source_file, target_file, dict_file, '%s.txt' % out_file)
    


if __name__ == '__main__':
    main(sys.argv)

