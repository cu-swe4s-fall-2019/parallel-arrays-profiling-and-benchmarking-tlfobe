import unittest
import os
import data_viz
import stat


class TestBoxPlot(unittest.TestCase):
    def test_boxplot_null(self):
        self.assertRaises(TypeError,
                          data_viz.boxplot,
                          None,
                          )

    def test_boxplot_empty_list(self):
        self.assertRaises(IndexError,
                          data_viz.boxplot,
                          [],
                          )

    def test_boxplot_wrong_type(self):
        self.assertRaises(TypeError, data_viz.boxplot, 'string', 'file.png')
        self.assertRaises(TypeError, data_viz.boxplot, dict(), 'file.png')
        self.assertRaises(TypeError, data_viz.boxplot, True, 'file.png')

    def test_boxplot_list_wrong_type(self):
        self.assertRaises(TypeError, data_viz.boxplot,
                          ['string', 1, 2, ['List!'], ],
                          )

    def test_boxplot_filename_str(self):
        self.assertRaises(TypeError, data_viz.boxplot,
                          [[1, 2, 3], [4, 5, 6], [7]],
                          1,
                          )

    def test_boxplot_write_to_file(self):
        data_viz.boxplot([[1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]],
                         'newfile.png',  names=["test"])
        self.assertTrue(os.path.exists("newfile.png"))
        os.remove("newfile.png")

    def test_boxplot_permission(self):
        with open("read_only.png", "w") as f:
            f.write("Hello, World!")
        os.chmod("read_only.png", stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)
        self.assertRaises(PermissionError, data_viz.boxplot, [
                          [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]], "read_only.png",
                          names=["yes"]
                          )
        os.remove("read_only.png")

    def test_boxplot_wrong_file(self):
        self.assertRaises(ValueError, data_viz.boxplot,
                          [[1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]],
                          "read_only.txt", names=["test"])
