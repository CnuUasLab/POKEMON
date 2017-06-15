#==============================================================#
#                                                              #
#    Description: This is the class to interact with the ftp   #
#      server and grab all of the files that are in the        #
#      directory. All should be jpg files.                     #
#                                                              #
#                Author: davidkroell                           #
#               Version: 0.0.1                                 #
#                                                              #
#==============================================================#
import ftplib
import thread

#===================================================
#
# Constructor for the IMG client over the
#   file transfer protocol library
#
#---------------------params:-----------------------
#
#    pHost - Host of the ftp server
#    pUser - Default: None - authenticate username
#    pPass - Default: None - authenticate password
#
#===================================================
class IMGClient():
    def __init__(self, pHost, pUser=None, pPass=None):
        self.url = pHost
        self.ftp = ftplib.FTP(self.url)

        self.img_lib = {}
        self.files = ["."]
        try:
            self.files = ftp.nlst()
        except ftplib.error_perm, resp:
            if str(resp) == "550 No files found":
                print "Error no files found in the directory."
            else:
                raise

        thread.start_new_thread(self.streamFiles, ())
        self.updating = False


    #==============================
    #
    #  Stream the files from the
    #   ftp server continuously
    #
    #==============================
    def streamFiles(self):
        while True:
            try:

                self.files = ftp.nlst()

                self.updating = True

                for f in files:
                    file = None
                    self.ftp.retrbinary("RETR " + f, file = open(f, 'wb').write)
                    self.img_lib[str(f)] = file
                    
                self.updating = False
                
            except ftplib.error_perm, resp:

                if str(resp) == "550 No files found":
                    print "Error no files found in the directory."
                else:
                    raise

    #=================================
    #
    # Retrieve the file list that is
    #  populated in the streaming
    #  thread. If it's not updating,
    #  then we retrieve it.
    #
    #=================================
    def getFileList(self):
        while(self.updating):
            pass

        return self.img_lib
        
        
        

        
