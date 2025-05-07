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
    st.write("Enter text in one orthography to see it in all other orthography.")
    
    # Input text area
    input_text = st.text_area("Input text", height=150, value="Dáagw dámaan X̱aad Kíhl ta ḵ'áalangaay gudáng?")
    
    # Select input scheme
    input_scheme = st.selectbox(
        "Input orthography",
        Converter.INPUT_SCHEMES
    )

    converter = Converter()
    
    # Process button
    if st.button("Convert"):
        if input_text:
            # Process the text
            st.subheader("Transliteration Results:")
            
            # Create custom table header with columns (1:3 ratio)
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown("**Orthography**")
            with col2:
                st.markdown("**Transliteration**")
            
            # Add a divider line
            st.markdown("---")
            
            # Display results row by row
            for scheme in Converter.SCHEMES:
                converted_text = converter.convert_transliteration(input_text, input_scheme, scheme)
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown(f"**{scheme}**")
                with col2:
                    st.text(converted_text)
                
                # Add a light divider between rows
                st.markdown("---")
        else:
            st.warning("Please enter some text to convert.")


if __name__ == "__main__":
    main()