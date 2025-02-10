import numpy as np
from collections import Counter
import qutip as qt
from qutip.core.gates import rx, ry, rz



def flip_bits(bitstring):
    """
    Flips all bits in a bitstring ('0' -> '1' and '1' -> '0').

    Parameters:
    - bitstring: string of '0' and '1'

    Returns:
    - Flipped bitstring
    """
    return ''.join('1' if bit == '0' else '0' for bit in bitstring)

def index_to_bitstring(index, num_bits):
    """
    Converts an index into a binary string of fixed length.

    Parameters:
    - index: integer, the index to convert (0 to len(p)-1)
    - num_bits: integer, the length of the bitstring

    Returns:
    - Bitstring representation of the index
    We flip to match pulser convention
    
    """
    
    return flip_bits(format(index, f'0{num_bits}b'))

def generate_bitstrings(p):
    """
    Generates a list of bitstrings corresponding to indices from 0 to len(p)-1.

    Parameters:
    - p: list of probabilities

    Returns:
    - List of bitstrings
    """
    num_bits = (len(p) - 1).bit_length()  # Compute the necessary bit length
    return [index_to_bitstring(i, num_bits) for i in range(len(p))]


def sample_bitstrings(p, N):
    """
    Samples N outcomes based on the probability vector p and returns a list of bitstrings.

    Parameters:
    - p: list or numpy array of probabilities [p_0, p_1, p_2, p_3]
    - N: number of samples

    Returns:
    - list of sampled bitstrings
    """
    bitstrings = generate_bitstrings(p)
    
    # Sample indices according to probability distribution
    sampled_indices = np.random.choice(len(p), size=N, p=p)
    
    # Convert indices to corresponding bitstrings
    register = [bitstrings[i] for i in sampled_indices]
    
    return np.array(register)


def count_bitstring_occurrences(bitstring_list):
    """
    Creates a dictionary mapping bitstrings to their occurrence counts in the list.

    Parameters:
    - bitstring_list: list of bitstrings (e.g., ['00', '01', '10', '11', '00', '10'])

    Returns:
    - Dictionary {bitstring: count}
    """
    return dict(Counter(bitstring_list))


def bitstrings_to_bitlists(bitstrings: np.ndarray):
    return np.array([list(map(int, bit)) for bit in bitstrings])


def sample_psi(psi: qt.Qobj, n_samp: int) -> np.ndarray:
    prob = (np.abs(psi.full())**2).reshape(-1)
    bitstrings = sample_bitstrings(prob.reshape(-1), n_samp)
    outcomes = bitstrings_to_bitlists(bitstrings)
    return outcomes, bitstrings 


def prerotation(psi: qt.Qobj, 
                basis: str, 
                NQ: int) -> qt.Qobj:
    if basis == 'X':
        rot = qt.tensor([ry(-np.pi/2)]*NQ)
        return rot * psi
    elif basis == 'Y':
        rot = qt.tensor([rx(np.pi/2)]*NQ)
        return rot * psi
    elif basis == 'Z':       
        return psi