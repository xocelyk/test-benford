import streamlit as st
import math

st.title('Is your dataset Benford?')

BENFORD = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]
def get_first_digit(num, idx=0):
    num = str(num)
    if idx >= len(str(num)):
        return None
    if num[idx] in [str(i) for i in range(1,10)]:
        return num[idx]
    else:
        return get_first_digit(num, idx+1)



def chi_square_test(data_count, expected_counts):
  """Return boolean on chi-square test (8 DOF & P-val=0.05)."""
  chi_square_stat = 0; # chi-square test statistic
  for data, expected in zip(data_count, expected_counts):
    chi_square = math.pow(data - expected, 2)
    chi_square_stat += chi_square / expected

  st.write("\nChi Squared Test Statistic = {:.3f}".format(chi_square_stat))
  st.write("Critical value at P-value of 0.05 is 15.51")
  if chi_square_stat < 15.51:
    st.write("Chi-square test passed")
  else:
    st.write("Chi-square test failed")


def get_expected_counts(total_count):
  """Return a list of expected Benford's law counts for a total sample count."""
  return [round(p * total_count/ 100) for p in BENFORD]

uploaded_file = None
uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False)
if uploaded_file is not None:
    bytes_data = str(uploaded_file.read(), 'utf-8')
    row_data = []
    data = bytes_data[1:].split('\n')
    for line in data:
	    row_data.append(line.split(','))

    col_names = row_data[0]

    col = st.radio('Select a column', col_names)
    col_idx = row_data[0].index(col)
    col_data = []
    row_idx = 1
    while len(row_data[row_idx]) == len(col_names):
        row = row_data[row_idx]
        col_data.append(row[col_idx])
        row_idx += 1
    
    digits_dict = {str(i): 0 for i in range(1, 10)}
    for row in col_data:
        num = str(row)
        digit = get_first_digit(num)
        if digit:
            digits_dict[digit] += 1

    total_entries = sum(digits_dict.values())
    try:
        expected_counts = get_expected_counts(total_entries)
        st.write(chi_square_test(digits_dict.values(), expected_counts))

        st.subheader('Your results')
        st.bar_chart(digits_dict.values())
        st.subheader('Expected results')
        st.bar_chart(expected_counts)
    except:
        st.write('Insufficient data to run test')





