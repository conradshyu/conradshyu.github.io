<?php
/*
 * Conrad Shyu (conrad.shyu@nih.gov)
 *
 * Bioinformatics and Computational Biological Sciences Branch (BCBB)
 * National Institute of Allergy and Infectious Diseases (NIAID)
 * National Institute of Health (NIH)
 * Rockville, MD 20852
 *
 * Last updated on 9/28/2020
*/

class bdfacs {
    public SimpleXMLElement $xml;
    public string $attr = "attr ";

    public function __construct(
        string $i = '<bdfacs version="Version 5.0.1" release_version="Version 5.0.1"/>')
    {
        $this->xml = new SimpleXMLElement('<?xml version="1.0" encoding="UTF-8"?>' . $i);
    }   // initialize XML structure

    private function json2xml(
        SimpleXMLElement $o,    // pointer to the XML structure
        array $a)               // array for XML contents
    {
        foreach($a as $k => $v) {
            if (is_array($v)) {
                $new_obj = $o->addChild($k);
                $this->json2xml($new_obj, $v);
            } else {
                if (strpos($k, $this->attr) !== false){
                    $o->addAttribute(substr($k, strlen($this->attr)), $v);
                } else {
                    $o->addChild($k, $v);
                }
            }
        }

        return($o);
    }   // convert json to xml

    public function SetHeader(
        string $tray = "one cell",
        string $d_info = "BDFACS Flow Cytometry Template Editor",
        string $o_info = "BCBB NIAID",
        string $note = "Developed by BCBB")
    {
        $a = array(
            "metadata" => array(
                "bd_supplied" => "false",
                "user_locked" => "false",
                "designer_info" => $d_info,
                "operator_info" => $o_info,
                "study" => array("notes" => $note)
            ),
            "experiment" => array(
                "attr name" => "",
                "date" => date("Y-m-j\TH:i:s"),
                "is_use_global_settings" => "true",
                "log_decades" => 4,
                "export_time" => date("Y-m-j\TH:i:s"),
                "tray" => array(
                    "attr name" => $tray,
                    "attr tray_type" => 0,
                    "attr rows" => 8,
                    "attr cols" => 12,
                    "attr Orientation" => 0,
                    "children_shown" => "false",
                    "HTSMode" => "false",
                    "Orientation" => 0,
                    "instrument_settings" => array(
                        "attr name" => "Instr Settings",
                        "attr template" => "true",
                        "threshold_op" => 2,
                        "flow_rate" => 0,
                        "auto_compensation" => "false",
                        "compensation_enabled" => "true",
                        "setup_date" => date("Y-m-j\TH:i:s"),
                        "scales_recorded" => "false",
                        "use_auto_biexp_scale" => "true"
                    )
                )
            )
        );

        return($this->json2xml($this->xml, $a));
    }   // set the XML header

    public function SetFooter()
    {
        $a = array(
            "carousel_mgr" => array(
                "is_layout_locked" => "false",
                "carousel_assign_states" => "FFFFFFFFFFFFFFFF",
                "acq_settings" => array(
                    "acq_time" => 3,
                    "is_start_mix" => "false",
                    "is_interim_mix" => "false",
                    "num_tubes_mix" => 4
                )
            )
        );

        return($this->json2xml($this->xml->experiment, $a));
    }   // set the XML footer

    public function SetLayout(
        string $s,      // name of the tray/experiment
        array $a)       // list of specimen and well(s) or tube(s)
    {
        $x = $this->xml->experiment->tray->addChild("loader_user_info");
        $b = array(
            "sample_flow_rate" => 1.5, "sample_volume" => 100,
            "record_sample_volume" => 100, "mixing_volume" => 100,
            "mixing_speed" => 200, "number_mixes" => 3, "wash_volume" => 400);

        foreach ($b as $i => $v) {
            $x->addAttribute($i, $v);
        }   // add attribute names

        $t = $this->xml->experiment->tray->addChild("layout_description");

        foreach($a as $i => $v) {
            foreach(array_keys($v) as $j) {
                $q = array();

                if (strlen($v[$j]["treatment"]) > 0) {
                    $q[] = $v[$j]["treatment"];
                }   // add treatment tag if available

                if (strlen($v[$j]["tag"]) > 0) {
                    $q[] = $v[$j]["tag"];
                }   // add optional tag if available

                $q[] = strtoupper($j);  // add well tag
                $w = $t->addChild("well");
                $w->addAttribute("x", $v[$j]["x"]);
                $w->addAttribute("y", $v[$j]["y"]);
                $w->addAttribute("name", sprintf(".%s.%s.%s", $s, $i, implode("_", $q)));
            }   // position of wells on tray
        }
    }   // set the well layout on tray

    public function SetExperiment(
        array $a)       // list of specimen and well(s) or tube(s)
    {
        $tube = array(
            "attr name" => "",
            "time_tick_last_event" => 0,
            "window_extension" => 0.0,
            "fsc_area_scaling" => 0.0,
            "acquirable" => "true",
            "institution" => "",
            "AcqObjInError" => "false",
            "AspiratedError" => "false",
            "loader_user_info" => array(
                "attr sample_flow_rate" => 1.5,
                "attr sample_volume" => 100,
                "attr record_sample_volume" => 100,
                "attr mixing_volume" => 100,
                "attr mixing_speed" => 200,
                "attr number_mixes" => 3,
                "attr wash_volume" => 400
            )
        );

        $gate = array(
            "gates" => array(
                "gate" => array(
                    "attr fullname" => "All Events",
                    "attr type" => "EventSource_Classifier",
                    "name" => "All Events",
                    "color" => "0x000000",
                    "visible" => "true",
                    "enabled" => "false",
                    "num_events" => 0
                )
            ),
            "pipeline" => array(
                "storage_gate" => "All Events",
                "color_counter" => 0,
                "stop_rule" => array(
                    "attr mode" => 1,
                    "attr time" => 0,
                    "attr gate" => "All Events",
                    "attr events" => 10000
                )
            ),
            "analysis" => array(
                "attr name" => "Analysis",
                "worksheet_config" => array(
                    "attr active_worksheet" => "Sheet1",
                    "attr active_acquisition_template" => "Global Sheet1",
                    "attr active_group" => "ACQUISITION_TEMPLATES"
                )
            ),
            "loader_user_info" => array(
                "attr sample_flow_rate" => 1.5,
                "attr sample_volume" => 100,
                "attr record_sample_volume" => 100,
                "attr mixing_volume" => 100,
                "attr mixing_speed" => 200,
                "attr number_mixes" => 3,
                "attr wash_volume" => 400
            )
        );

        $k1 = array(
            "keyword" => array(
                "attr name" => "SAMPLE ID",
                "attr type" => 2,
                "suffix" => "",
                "visible" => "true",
                "edit_name" => "true",
                "edit_name_only" => "false",
                "edit_value" => "true",
                "edit_limit" => "true",
                "length" => 64,
                "value" => ""
            )
        );

        $k2 = array(
            "keyword" => array(
                "attr name" => "PATIENT ID",
                "attr type" => 2,
                "suffix" => "",
                "visible" => "true",
                "edit_name" => "true",
                "edit_name_only" => "false",
                "edit_value" => "true",
                "edit_limit" => "true",
                "length" => 64,
                "value" => ""
            )
        );

        foreach($a as $i => $v) {
            $w = $this->xml->experiment->tray->addChild("specimen");
            $this->json2xml($w,
                array("attr name" => $i, "is_auto_comp" => "false", "is_calibration_control" => "false"));

            foreach(array_keys($v) as $j) {
                $u = array();

                if (strlen($v[$j]["treatment"]) > 0) {
                    $u[] = $v[$j]["treatment"];
                }   // add treatment to well

                if (strlen($v[$j]["tag"]) > 0) {
                    $u[] = $v[$j]["tag"];
                }   // add optional tag to well

                $u[] = strtoupper($j);
                $tube["attr name"] = implode("_", $u);
                $t = $w->addChild("tube");
                $this->json2xml($t, $tube);
                $this->json2xml($t->addChild("keywords"), $k1);
                $this->json2xml($t->keywords, $k2);
                $this->json2xml($t, $gate);
            }
        }

        return($this->xml);
    }   // set the XML contents for experiments

    public function Dump()
    {
        $dom = dom_import_simplexml($this->xml)->ownerDocument;
        $dom->formatOutput = true;
        echo $dom->saveXML();
    }   // output the XML

    public function Export($f)
    {
        $this->xml->asXML($f);
        return(printf($f));
    }   // write the XML file
}   // bdfacs cytometry XML editor

function SetData(array $j)
{
    $set = array();

    foreach($j as $k => $v) {
        if (strlen($v["specimen"]) == 0) {
            continue;
        }   // skip wells with empty specimen

        $set[str_replace(" ", "_", $v["specimen"])][$k] = array(
            "treatment" => str_replace(" ", "_", $v["treatment"]),
            "tag" => str_replace(" ", "_", $v["tag"]),
            "x" => $v["x"], "y" => $v["y"]);
    }   // consolidate the wells

    return($set);
}   // consolidate the data

$j = SetData(json_decode($_POST["json"], true));

$x = new bdfacs();
$x->SetHeader($_POST["tray"], "", "", "");

if (count($j) > 0) {
    $x->SetExperiment($j);
    $x->SetLayout($_POST["tray"], $j);
}   // tray is empty

$x->SetFooter();
$x->Dump();

?>
