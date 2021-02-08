from pathlib import *
import sysdynpy.utils as utils
import json
import csv
import matplotlib.pyplot as plt

class Exporter(utils.SubclassOnlyABC):
    """This abstract class can be used to export simulation results to different formats
    """

    _supported_formats = ["csv", "json", "jpg", "png"]
    """ A private list of supported file formats. Can be used to validate a given input format.
    """

    @classmethod
    def export_data(cls, results, file_format, system_elements, rel_path="./results"):
        """TODO
        rel path: .\\somepath  ./somepath  somepath ../somepath ..\\somepath
        """
        out_path, results_filtered = None, None
        try:
           out_path, results_filtered = \
                cls._prepare_export(results, file_format, system_elements, rel_path)
        except ValueError as v:
            raise v
        
        if file_format == "csv":
            with open(out_path, "w", encoding="utf-8", newline='') as outfile:
                writer = csv.writer(outfile, delimiter=";")
                writer.writerow(results_filtered.keys())
                writer.writerows(zip(*results_filtered.values()))

        if file_format == "json":
            with open(out_path, "w", encoding="utf-8", newline='') as outfile:
                json.dump(results_filtered, outfile, ensure_ascii=False)
              

        
    @classmethod
    def export_graph(cls, results, file_format, system_elements, \
        range_x, range_y, colors, title="", label_x="", label_y="", line_width=1,
        legend_pos="upper left", rel_path="results",):
        """TODO
        rel path: .\\somepath  ./somepath  somepath ../somepath ..\\somepath
        """

        out_path, results_filtered = None, None
        try:
           out_path, results_filtered = \
                cls._prepare_export(results, file_format, system_elements, rel_path)
        except ValueError as v:
            raise v
        
        for key in results_filtered:
            data_x = range(len(results_filtered[key]))
            data_y = results_filtered[key]
            # get position of current key in system_elements so we can set the right color
            idx = system_elements.index(key)
            plt.plot(data_x, data_y, color=colors[idx], \
                linewidth=line_width, label=key)
        
        plt.title(title)
        plt.xlabel(label_x)
        plt.ylabel(label_y)
        plt.xlim(range_x)
        plt.ylim(range_y)
        plt.legend(loc=legend_pos)
        #plt.show()
        plt.savefig(out_path)
        plt.clf()

    @classmethod
    def _prepare_export(cls, results, file_format, system_elements, rel_path):
        """Prepares the export. 

        Contains actions that have to be done regardless of export format.
        These actions include:
            - check if file format is supported
            - check if given system elements are in results
            - filter results to only contain given system elements
            - joins the given relative path to the location the script is executed from
        
        All these actions are done in separate methods.

        :param file_format: [description]
        :type file_format: [type]
        :param results: [description]
        :type results: [type]
        :param system_elements: [description]
        :type system_elements: [type]
        :param rel_path: [description]
        :type rel_path: [type]
        :raises v: [description]
        :raises v: [description]
        :return: [description]
        :rtype: [type]
        """
        # check if file format is supported
        try:
            cls._check_file_format(file_format)
        except ValueError as v:
            raise v

        # check if all given system elements are in results
        try:
            _check_if_system_elements_in_results(results, system_elements)
        except ValueError as v:
            raise v

         # filter results to only contain given system elements
        results_filtered = _filter_results(results, system_elements)
        
        # create file output path
        out_path = _create_abs_output_path(rel_path, file_format)

        return out_path, results_filtered

    @classmethod
    def _check_file_format(cls, file_format):
        if file_format.lower() not in cls._supported_formats:
            raise ValueError("Given file format '" + file_format
            + "' is not supported. Supported formats are: "
            + cls._supported_formats)

    
def _create_abs_output_path(rel_path, file_format):
    current_dir = Path.cwd()
    if file_format not in rel_path:
        rel_path += "." + file_format.lower()
    return (current_dir / rel_path).resolve()


def _check_if_system_elements_in_results(results, system_elements):
    for element in system_elements:
        if element not in results.keys():
            raise ValueError("Given system element "
                + element + " is not in simulation results")


def _filter_results(results, system_elements):
    results_filtered = {}
    for key in results.keys():
        if key in system_elements:
            results_filtered[key] = results[key]
    return results_filtered


if __name__ == "__main__":
    path = Exporter._create_abs_output_path("test", "csv")
    print(path)