from pathlib import *
import sysdynpy.utils as utils
import json
import csv
import matplotlib.pyplot as plt

class Exporter(utils.SubclassOnlyABC):
    """This abstract class can be used to export simulation results to different formats
    """

    supported_formats = ["csv", "json", "jpg", "png"]

    @classmethod
    def export_as(cls, file_format, sim_results, system_elements, rel_path):
        """TODO
        rel path: .\\somepath  ./somepath  somepath ../somepath ..\\somepath
        """

        # check if file format is supported
        if file_format.lower() not in cls.supported_formats:
            raise ValueError("Given file format '" + file_format
                + "' is not supported. Supported formats are: "
                + cls.supported_formats)
        
        # check if all given system elements are in results
        for element in system_elements:
            if element not in sim_results.keys():
                raise ValueError("Given system element "
                    + element.name + " is not in simulation results")
        
        out_path = _create_abs_output_path(rel_path, file_format)

        # filter keys
        sim_results_filtered = {}
        for key in sim_results.keys():
            if key in system_elements:
                sim_results_filtered[key] = sim_results[key]

        if file_format == "csv":
            print(sim_results_filtered)
            with open(out_path, "w", encoding="utf-8", newline='') as outfile:
                writer = csv.writer(outfile, delimiter=";")
                writer.writerow(sim_results_filtered.keys())
                writer.writerows(zip(*sim_results_filtered.values()))

        if file_format == "json":
            with open(out_path, "w", encoding="utf-8", newline='') as outfile:
                json.dump(sim_results_filtered, outfile, ensure_ascii=False)
                
        if file_format == "jpg" or file_format == "png":
            for key in sim_results_filtered:
                data_x = range(len(sim_results_filtered[key]))
                data_y = sim_results_filtered[key]
                plt.plot(data_x, data_y)
            
            plt.title('SomeDiagram')
            plt.xlabel('Time')
            plt.ylabel('Stocks')
            # plt.show()
            plt.savefig(out_path)



def _create_abs_output_path(rel_path, file_format):
    current_dir = Path.cwd()
    if file_format not in rel_path:
        rel_path += "." + file_format
    return (current_dir / rel_path).resolve()


if __name__ == "__main__":
    path = Exporter._create_abs_output_path("test", "csv")
    print(path)