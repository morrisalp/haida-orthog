import streamlit as st
from orthog import Converter


def main():
    
    st.set_page_config(
        page_title="Haida Transliterator",
        # page_icon="🔤",  # Optional: you can use an emoji or leave this out
        # layout="centered",  # Optional: "centered" or "wide"
        # initial_sidebar_state="auto"  # Optional: "auto", "expanded", or "collapsed"
    )

    st.title("Haida Orthography Converter")
    st.write("Enter text in one scheme to see it in all other schemes.")
    
    # Input text area
    input_text = st.text_area("Input text", height=150, value="Dáagw dámaan X̱aad Kíhl ta ḵ'áalangaay gudáng?")
    
    # Select input scheme
    input_scheme = st.selectbox(
        "Input scheme",
        Converter.SCHEMES
    )

    converter = Converter()
    
    # Process button
    if st.button("Convert"):
        if input_text:

            # Process the text
            st.subheader("Transliteration Results:")
            
            # Display output in each scheme
            for scheme in Converter.SCHEMES:
                # if scheme != input_scheme:
                st.write(f"**{scheme} scheme:**")
                converted_text = converter.convert_transliteration(input_text, input_scheme, scheme)
                st.text(converted_text)
        else:
            st.warning("Please enter some text to convert.")

if __name__ == "__main__":
    main()