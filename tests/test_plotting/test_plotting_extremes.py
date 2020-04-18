# pyextremes, Extreme Value Analysis in Python
# Copyright (C), 2020 Georgii Bocharov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import itertools
import os
import pathlib

import matplotlib
import matplotlib.testing.compare
import pandas as pd
import pytest

from pyextremes.plotting import plot_extremes

matplotlib.use('agg')

module_path = pathlib.Path(os.path.realpath(__file__)).parent
test_data_folder = module_path.parent / 'data'
test_data = pd.read_csv(test_data_folder/'battery_wl.csv', index_col=0, parse_dates=True, squeeze=True)


@pytest.mark.parametrize('extremes_method, extremes_type', list(itertools.product(['BM', 'POT'], ['high', 'low'])))
def test_plot_extremes(extremes_method, extremes_type):
    test_extremes = pd.read_csv(
        test_data_folder/f'extremes_{extremes_method.lower()}_{extremes_type}.csv',
        index_col=0, parse_dates=True, squeeze=True
    )
    fig, ax = plot_extremes(
        ts=test_data,
        extremes=test_extremes,
        extremes_method=extremes_method,
        extremes_type=extremes_type,
        block_size={
            'BM': '1Y',
            'POT': None
        }[extremes_method],
        figsize=(8, 5)
    )
    baseline_figure = module_path / 'baseline_images' / f'plot_extremes_{extremes_method}_{extremes_type}.png'
    generated_figure = module_path / 'baseline_images' / f'plot_extremes_{extremes_method}_{extremes_type}_compare.png'
    fig.savefig(generated_figure, dpi=96)
    matplotlib.testing.compare.compare_images(
        expected=str(baseline_figure),
        actual=str(generated_figure),
        tol=.001
    )
    generated_figure.unlink()