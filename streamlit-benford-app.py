import streamlit as st

st.title('Is your dataset Benford?')
st.write('Upload a data file and choose a column to analyze. We\'ll do a chi-square test to see if the data follows Benford\'s Law.')

BENFORD = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]

def get_first_digit(num, idx=0):
    num = str(num)
    if idx >= len(str(num)):
        return None
    if num[idx] in [str(i) for i in range(1,10)]:
        return num[idx]
    else:
        return get_first_digit(num, idx+1)

from scipy.stats import chi2

def calculate_p_value(chi_square_stat, df):
    # Calculate p-value
    p_value = 1 - chi2.cdf(chi_square_stat, df)
    return p_value

    
def calculate_chi_square(observed, expected):
  chi_square_stat = 0  # chi square test statistic
  for data in zip(observed, expected):
      if data[1] == 0:  # to avoid division by zero
          continue
      chi_square = pow(data[0] - data[1], 2) / data[1]
      chi_square_stat += chi_square
  return chi_square_stat

def chi_square_test(observed_frequencies, expected_counts):
    chi_square_stat = calculate_chi_square(observed_frequencies, expected_counts)
    p_value = calculate_p_value(chi_square_stat, len(observed_frequencies) - 1)
    st.write("Chi-square statistic = {:.1f}, p-value = {:.3f}".format(chi_square_stat, p_value))
    if p_value > 0.05:
        st.write('The data follows Benford\'s Law')
    else:
        st.write('The data does not follow Benford\'s Law')

def get_expected_counts(total_count):
    """Return a list of expected Benford's law counts for a total sample count."""
    expected_counts = [p * total_count / 100 for p in BENFORD]
    return expected_counts

uploaded_file = None
uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False)
if uploaded_file is not None:
    bytes_data = str(uploaded_file.read(), 'utf-8')
    row_data = []
    data = bytes_data[:].split('\n')
    for line in data:
        row_data.append(line.split(','))
    col_names = row_data[0]

    col = st.radio('Select a column', col_names)
    col_idx = row_data[0].index(col)
    col_data = []

    for row in row_data[1:]: # start from the second row
        if len(row) == len(col_names):
            col_data.append(row[col_idx])

    digits_dict = {str(i): 0 for i in range(1, 10)}
    for row in col_data:
        num = str(row)
        digit = get_first_digit(num)
        if digit:
            digits_dict[digit] += 1

    # Ensure the observed frequencies are in correct order
    observed_frequencies = [digits_dict[str(i)] for i in range(1, 10)]

    total_entries = sum(observed_frequencies)
    try:
        expected_counts = get_expected_counts(total_entries)
        res = chi_square_test(observed_frequencies, expected_counts)
    except:
        st.write('Insufficient data to run test')
    
    if True:
      st.subheader('First digit distribution of your data')
      st.bar_chart([0] + list(digits_dict.values()))
      st.subheader('Expected Benford distribution')
      st.bar_chart([0] + expected_counts)
