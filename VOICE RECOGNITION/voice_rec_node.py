#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

def main():
    # Initialize ROS node
    rospy.init_node('pocketsphinx_node')
    pub = rospy.Publisher('recognized_speech', String, queue_size=10)

    # Initialize GStreamer
    Gst.init(None)

    pipeline = Gst.parse_launch('autoaudiosrc ! audioconvert !' +
                                ' audioresample ! pocketsphinx name=asr !' +
                                ' fakesink')

    pocketsphinx = pipeline.get_by_name('asr')
    pocketsphinx.set_property('hmm', '/home/sangwan7gaurav/catkin_ws/src/pocketsphinx/model/en-us/en-us')
    pocketsphinx.set_property('lm', '/home/sangwan7gaurav/catkin_ws/src/pocketsphinx/model/en-us/cst.lm')
    pocketsphinx.set_property('dict', '/home/sangwan7gaurav/catkin_ws/src/pocketsphinx/model/en-us/cst.dic')

    bus = pipeline.get_bus()
    bus.add_signal_watch()

    pipeline.set_state(Gst.State.PLAYING)

    while not rospy.is_shutdown():
        msg = bus.timed_pop(Gst.CLOCK_TIME_NONE)
        if msg:
            if msg.type == Gst.MessageType.EOS:
                break
            struct = msg.get_structure()
            if struct and struct.get_name() == 'pocketsphinx':
                final = struct.get_value('final')
                hypothesis = struct.get_value('hypothesis')
                if final:
                    rospy.loginfo("Recognized: %s", hypothesis)
                    pub.publish(hypothesis)

    pipeline.set_state(Gst.State.NULL)

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass