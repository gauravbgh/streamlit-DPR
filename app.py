import streamlit as st
from model import DPR

def main():
    
    html_temp = """
    <div style="background-color:#025246 ;padding:10px">
    <h2 style="color:white;text-align:center;"> AL DPR </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    
    ar1 = st.text_area("AREA-1","Type Here")
    ar3 = st.text_area("AREA-3","Type Here")
    ar4 = st.text_area("AREA-4","Type Here")
    
    
    if st.button("Genenrate"):
        
        ar1_list = ar1.split("\n")
        ar3_list = ar3.split("\n")
        ar4_list = ar4.split("\n")
        
        model_load = DPR(ar1_list, ar3_list, ar4_list)
        abb= model_load.predict() 
        
        st.text_area('COMPILED', abb, height=500)
        


if __name__=='__main__':
    main()