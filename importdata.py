import csv, sys

class InstitutionData(object):

    def __init__(self, filename, specialty, prog_type, rm_headings = 1):
        self.filename = filename
        self.specialty = specialty
        self.prog_type = prog_type
        self.rm_headings = rm_headings
        self.data = []
        self.finaldata = []

    def read_data_file(self):
        reader = csv.reader(open(self.filename, "U"))
        try:
            for row in reader:
                self.data.append(row)
                #print row
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

    def prep_data(self):
        if self.rm_headings:
            del self.data[0]  # removes the column headings
        for row in self.data:
            row[3] = int(row[3])
            row[5] = int(row[5])
            row[6] = int(row[6])
            row[7] = int(row[7])
        [_f for _f in self.data[6] if _f]
        #for (i,x) in enumerate(self.data):
            #if x[6] == 0: self.data.pop(i)
        #[x for x in self.data if x[6] !=0]


    def select_data(self):
        self.finaldata = [inst for inst in self.data if inst[3] == self.specialty and inst[4] == self.prog_type]
        print(('Selecting_data', 'Specialty =', self.specialty, 'Type =', self.prog_type))
        print('Before selecting data', len(self.data), 'Institutions, After Selecting data', len(self.finaldata))

    #def get_data(self):
        #read_data_file()
        #prep_data()
        #select_data()
