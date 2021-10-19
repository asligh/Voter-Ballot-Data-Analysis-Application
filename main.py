import os
import csv

#Author: Ashley Sligh

#Date: 10/08/2021

#Purpose: Processes election ballot records and prints election totals, percentages by incumbent, and winner.

#Dependencies: Election ballot flat input file

#Stored Procedures: None

#Referenced Tables: None

class Program():

    ###################
    #                 # 
    #   PRIVATE VARS  #
    #                 # 
    ###################

    __VOTER_ID_IDX        = 0                           #Stores the voter id index
    __COUNTY_IDX          = 1                           #Stores the county index
    __CANDIDATE_IDX       = 2                           #Stores the candidate index
    __IN_FILE_NAME        = "election_data.csv"         #Stores the input file name
    __OUT_FILE_NAME       = "election_data_analysis"    #Stores the output file name
    __OUT_FILE_EXTENSION  = ".txt"                      #Stores the input file extension
    __IN_FOLDER_NAME      = "Resources"                 #Stores the input file folder
    __OUT_FOLDER_NAME     = "analysis"                  #Stores the output file folder
  
    __election_results = {}     #Stores election results
    __total_vote_count = None   #Stores the total number of cast election votes

    ###################
    #                 # 
    #     GETTERS     #
    #                 # 
    ###################

    #Returns the input file name
    def get_in_file_name(self):
        return self.__IN_FILE_NAME

    #Returns the output file name
    def get_out_file_name(self):
        return self.__OUT_FILE_NAME    
        
    #Returns the input folder name
    def get_in_folder_name(self):
        return self.__IN_FOLDER_NAME  

    #Returns the output folder name
    def get_out_folder_name(self):
        return self.__OUT_FOLDER_NAME   

    #Returns the output file extension
    def get_out_file_extension(self):
        return self.__OUT_FILE_EXTENSION     

    #Returns the voter id index
    def get_voter_id_idx(self):
        return self.__VOTER_ID_IDX  

    #Returns the county index
    def get_county_idx(self):
        return self.__COUNTY_IDX        

    #Returns the candidate index
    def get_candidate_idx(self):
        return self.__CANDIDATE_IDX  

    #Returns the total vote count
    def get_total_vote_count(self):
        return self.__total_vote_count

    #Returns election results
    def get_election_results(self):
        return self.__election_results   

    #Returns input file path
    def get_in_file_path(self):
        in_folder_name = self.get_in_folder_name()
        in_file_name   = self.get_in_file_name()
        return os.path.join(in_folder_name, in_file_name).replace("\\", "/")

    #Returns output file path
    def get_out_file_path(self):
        out_folder_name    = self.get_out_folder_name()
        out_file_name      = self.get_out_file_name()
        out_file_extension = self.get_out_file_extension()
        return os.path.join(out_folder_name, out_file_name + out_file_extension).replace("\\", "/")    
    
    ###################
    #                 # 
    #     SETTERS     #
    #                 # 
    ###################

    #Stores election results
    def set_election_results(self,election_results):
        self.__election_results = election_results

    #Stores total vote count
    def set_total_vote_count(self,total_vote_count):
        self.__total_vote_count = total_vote_count

    #Reads input file data and stores into the election results variable for future processing and analysis
    def read_data(self):
        
        election_results = {} #self.get_election_results()
        in_file_path  = self.get_in_file_path()

        with open(in_file_path, 'r') as in_file:

            records = csv.reader(in_file, delimiter=',') 

            header_row = next(records) # store header row for future use

            for record in records:

                candidate = record[self.get_candidate_idx()]    

                if candidate not in list(election_results.keys()): 
                    election_results.update({candidate:1})
                else:
                    election_results.update({candidate : int(election_results[candidate]) + 1})

            self.set_total_vote_count(sum(election_results.values()))

            #source: https://thispointer.com/sort-a-dictionary-by-value-in-python-in-descending-ascending-order/
            election_results = dict(sorted(election_results.items(),key = lambda x : x[1],reverse=True)) #not in-situ

            self.set_election_results(election_results)

    #Returns election winner
    def get_election_winner(self) -> str:
        election_results = self.get_election_results()

        #source: https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
        election_winner = max(election_results,key=election_results.get)

        return election_winner

    #Returns election winner for end-user display purposes
    def get_election_winner_for_display(self) -> str:
        return f"Winner: {self.get_election_winner()}{self.get_new_line()}"   

    #Returns election anlaysis for a given candidate
    def get_analysis_by_candidate(self,candidate) -> str:

        election_results = self.get_election_results()
        vote_count = election_results[candidate]

        #Source: https://stackoverflow.com/questions/6149006/how-to-display-a-float-with-two-decimal-places
        pct_of_tot_vote = "{0:.3f}".format(vote_count / self.get_total_vote_count() * 100) + "%"

        return f"{candidate}: {pct_of_tot_vote} ({vote_count}){self.get_new_line()}"

    #Returns the election results data analysis
    def get_data_analysis(self) -> str:

        election_results = self.get_election_results()

        print_str = f"Election Results{self.get_new_line()}" \
        + f"{self.get_line_separator(True)}" \
        + f"{self.get_total_votes_for_display()}" \
        + f"{self.get_line_separator(True)}"                                             

        for key in election_results.keys():
            print_str += self.get_analysis_by_candidate(key)

        print_str += f"{self.get_line_separator(True)}" 
        print_str += f"{self.get_election_winner_for_display()}"
        print_str += f"{self.get_line_separator(False)}" 

        return print_str

    #Returns a line separator    
    def get_line_separator(self,include_new_line) -> str:
        if include_new_line:
            return f"-------------------------{self.get_new_line()}"
        else:
            return f"-------------------------"

    #Returns a new-line char
    def get_new_line(self) -> str:
        return "\n"

    #Returns the total number of votes cast for end-user display purposes
    def get_total_votes_for_display(self) -> str:
        return f"Total Votes: {self.get_total_vote_count()}{self.get_new_line()}"
    
    #Prints data to the terminal window
    def write_data_to_terminal(self):
        print(self.get_data_analysis())

    #Writes data to pre-specified output file
    def write_data_to_file(self):
        out_file_path  = self.get_out_file_path()

        with open(out_file_path, "w") as out_file:
            out_file.write(self.get_data_analysis())

    #End Class

#Main program repsonsible for running application
def run_program():

    program = Program()
    status = 0
 
    try:
        program.read_data()
        program.get_total_vote_count()
        program.get_election_winner()
        program.write_data_to_terminal()
        program.write_data_to_file()

    except IOError as e:
        print(e.__str__())
        status = -1

    return status

result = run_program()