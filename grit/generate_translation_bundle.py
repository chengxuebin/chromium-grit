# -*- coding: utf-8 -*

'''Bootstrapping for GRIT.
'''

import os
import sys
#import argparse
import optparse
import grit.grit_runner
import xml.dom.minidom
import xml.etree.ElementTree as ET

def PrintUsage():
  print( """xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Usage: grit [GLOBALOPTIONS] TOOL [args to tool]

Global options:

  -i INPUT  Specifies the INPUT file to use (a .grd file).  If this is not
            specified, GRIT will look for the environment variable GRIT_INPUT.
            If it is not present either, GRIT will try to find an input file
            named 'resource.grd' in the current working directory.

  -h MODULE xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
""")

def _ParseOptions(): 
  #parser = argparse.ArgumentParser(description='Change file names.')
  parser = optparse.OptionParser()
  # metavar only changes the displayed name
  # first argument (w/o '-') used as positional argument
  # argument with '-' will be used as optional argument
  # nargs '?' will treat input as string, 
  # while '+' for list
  parser.add_option('--old_grd', 
                     help='original grd file')
  parser.add_option('--new_grd', 
                     help='modified grd file')
  parser.add_option('--old_xtb', 
                     help='original xtb file')                   
  parser.add_option('-o', '--output', 
                     help='output directory')                   
  # parse cmdline arguments to an object
  # then pass to main
  args, _  = parser.parse_args()
  if not args.old_grd:
    parser.error('You must provide a origin grd file.')
  if not args.new_grd:
    parser.error('You must provide a modified grd file.')
  if not args.old_xtb:
    parser.error('You must provide a origin xtb file.')    
  return args


#--------------------------------
# 读取 xml 文件，返回 dom 对象
def getXmlObj(filePath, mode):
  tree = ET.parse(filePath)
  root = tree.getroot()
  return root
     
def generateTranslationBundle(oldGrdPath, newGrdPath, oldXtbPath):
  oldGrdDoc = getXmlObj(oldGrdPath, 'r')
  newGrdDoc = getXmlObj(newGrdPath, 'r')
  oldXtbDoc = getXmlObj(oldXtbPath, 'r')
  
  #print len(oldGrdDoc.findall("msg[@desc='Error displayed on startup when user preferences file can not be read']"))
  print len(oldGrdDoc.findall("./msg[2]"))
         
def main(args):
  # 检查python版本
  if sys.version_info < (2, 6):
    print( "GRIT requires Python 2.6 or later." )
    return
    
  # 打印帮助  
  elif not args or (len(args) == 1 and args[0] == 'help'):
    PrintUsage()
    return 0
    
  options = _ParseOptions()  
    
  # 处理 old grd 文件
  #grit.grit_runner.Main(["-i", options.old_grd, "xmb","-D","_chromium", "-D", "toolkit_views", "-D", "remoting", "-D","enable_register_protocol_handler", options.output+'/old_grd.xtb' ])
  
  # 处理 new grd 文件
  #grit.grit_runner.Main(["-i", options.new_grd, "xmb","-D","_chromium", "-D", "toolkit_views", "-D", "remoting", "-D","enable_register_protocol_handler", options.output+'/new_grd.xtb' ])
  
  # 生成 new xtb 文件
  generateTranslationBundle(options.output+'/old_grd.xtb', options.output+'/new_grd.xtb', options.old_xtb);

# Omitted when being used as module
if '__main__' == __name__:   
  sys.exit(main(sys.argv[1:]))
