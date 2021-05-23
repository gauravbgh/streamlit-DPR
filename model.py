import re
import datetime


class DPR():
        
    def __init__(self,ar1_list,ar3_list,ar4_list):
        
        self.ar1_list= ar1_list
        self.ar3_list= ar3_list
        self.ar4_list= ar4_list
        
        return None
    
    def monitored_well(self,dpr_list):
        indx= dpr_list.index([ i for i in dpr_list if re.search('.*[mM]onitored.*', i)][0])
        mon_well= dpr_list[indx+1].rstrip('.')
        return (mon_well)
    
    def tpr(self, dpr_list):
        try:
            indx= dpr_list.index([ i for i in dpr_list if re.search('\*TPR.*', i)][0])
            if len(dpr_list[indx])>7:
                tpr= dpr_list[indx].split(' ')[-1]
                tpr= tpr.rstrip('.')
            else:
                tpr= dpr_list[indx+1].rstrip('.')
                tpr= tpr.replace(' ','')
            return(tpr)
        except IndexError:
            return ('')
        
    def remark(self, dpr_list):
        remarks=[]
        ind_remark= dpr_list.index([ i for i in dpr_list if re.search('\*[rR]emarks.*', i)][0])
        ind_pressure= dpr_list.index([ i for i in dpr_list if re.search('\*[wW]ell\s?head .*', i)][0])
        for i in range(1, (ind_pressure-ind_remark)):
            remark= dpr_list[ind_remark+i]
            key= re.search('(\d+.) (\*.+\*)(\s?:?\s?)(.+)', remark)
            well_no = (key.group(2)).strip('*').rstrip(':')
            remarks.append('*{0}:* {1}'.format(well_no, key.group(4)))
        return(remarks)
    
    def wellhead_press(self, dpr_list):
        start= dpr_list.index([ i for i in dpr_list if re.search('\*[wW]ell\s?head .*', i)][0])
        try:
            stop= dpr_list.index([ i for i in dpr_list if re.search('\*[tT]eam.*', i)][0])
        
        except IndexError:
            stop= dpr_list.index([ i for i in dpr_list if re.search('[rR]egard.*', i)][0])
       
        out= dpr_list[(start+1):stop]
        return(out)

    
    def predict(self):
        
        ar1_split= [x for x in self.ar1_list if len(x)>1]
        ar3_split= [x for x in self.ar3_list if len(x)>1]
        ar4_split= [x for x in self.ar4_list if len(x)>1]
        
        if len(ar4_split)>4:
            total_wells_monitored= self.monitored_well(ar1_split)+(',\n') + self.monitored_well(ar3_split) + (',\n') + self.monitored_well(ar4_split) + ('.')
            tpr_total= self.tpr(ar1_split) + (',') + self.tpr(ar3_split) + ('.') + self.tpr(ar4_split)
            total_remarks= self.remark(ar1_split)+self.remark(ar3_split)+self.remark(ar4_split)
            remarks_print= ''
            for i in range(len(total_remarks)):
                remarks_print= remarks_print + str(i+1) + ') ' + total_remarks[i]+ '\n'
            total_pressure= self.wellhead_press(ar1_split)+ self.wellhead_press(ar3_split)+ self.wellhead_press(ar4_split)
            pressures= ''
            for i in range(len(total_pressure)):
                pressures= pressures + total_pressure[i]+ '\n'
        
        else:
            
            total_wells_monitored= self.monitored_well(ar1_split)+(',\n')+self.monitored_well(ar3_split)+('.')
            tpr_total= self.tpr(ar1_split) + (',') + self.tpr(ar3_split) + ('.')
            total_remarks= self.remark(ar1_split)+ self.remark(ar3_split)
            remarks_print= ""
            for i in range(len(total_remarks)):
                remarks_print= remarks_print + str(i+1) + ') ' + total_remarks[i]+ '\n'
            
            total_pressure= self.wellhead_press(ar1_split)+ self.wellhead_press(ar3_split)
            pressures= ""
            for i in range(len(total_pressure)):
                pressures= pressures + total_pressure[i]+ '\n'
            
            
        abc= datetime.date.today()
        final= "Sir,\n*A/Lift DPR on {0}/{1}/{2}*\n*Wells Monitored*\n{3}\n*TPR:*\n{4}\n*Remarks:*\n{5}*Wellhead Pressure:*\n{6}Regards\nGairik Das".format(abc.day, abc.month, abc.year, total_wells_monitored, tpr_total, remarks_print,pressures)
        
        #out = final.split('\n')
        
        return(final)