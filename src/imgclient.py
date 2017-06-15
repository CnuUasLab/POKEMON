import ftplib
import thread

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

    def getFileList(self):
        while(self.updating):
            pass

        return self.img_lib
        
        
        

        
