#include <gazebo/physics/Model.hh>
#include <gazebo/physics/World.hh>
#include <gazebo/physics/Joint.hh>
#include <gazebo_ros/node.hpp>
#include <rclcpp/rclcpp.hpp>

#include "ros2_conveyorbelt/ros2_conveyorbelt_plugin.hpp"     // Header file.

#include <conveyorbelt_msgs/srv/conveyor_belt_control.hpp>    // ROS2 Service.
#include <conveyorbelt_msgs/msg/conveyor_belt_state.hpp>      // ROS2 Message.

#include <memory>

namespace gazebo_ros
{

class ROS2ConveyorBeltPluginPrivate
{
public:

  // ROS node for communication, managed by gazebo_ros.
  gazebo_ros::Node::SharedPtr ros_node_;

  // The joint that controls the movement of the belt:
  gazebo::physics::JointPtr belt_joint_;

  // Additional parametres:
  double belt_velocity_;
  double max_velocity_;
  double power_;
  double limit_;
  
  // PUBLISH ConveyorBelt status:
  void PublishStatus();                                                                     // Method to publish status.
  rclcpp::Publisher<conveyorbelt_msgs::msg::ConveyorBeltState>::SharedPtr status_pub_;      // Publisher.
  conveyorbelt_msgs::msg::ConveyorBeltState status_msg_;                                    // ConveyorBelt status.

  // SET Conveyor Power:
  void SetConveyorPower(
    conveyorbelt_msgs::srv::ConveyorBeltControl::Request::SharedPtr,    
    conveyorbelt_msgs::srv::ConveyorBeltControl::Response::SharedPtr);                      // Method to execute service.
  rclcpp::Service<conveyorbelt_msgs::srv::ConveyorBeltControl>::SharedPtr enable_service_;  // ROS2 Service.

  // WORLD UPDATE event:
  void OnUpdate();
  rclcpp::Time last_publish_time_;
  int update_ns_;
  gazebo::event::ConnectionPtr update_connection_;  // Connection to world update event. Callback is called while this is alive.

};

ROS2ConveyorBeltPlugin::ROS2ConveyorBeltPlugin()
: impl_(std::make_unique<ROS2ConveyorBeltPluginPrivate>())
{
}

ROS2ConveyorBeltPlugin::~ROS2ConveyorBeltPlugin()
{
}

void ROS2ConveyorBeltPlugin::Load(gazebo::physics::ModelPtr _model, sdf::ElementPtr _sdf)
{
  
  // Create ROS2 node:
  impl_->ros_node_ = gazebo_ros::Node::Get(_sdf);

  // OBTAIN -> BELT JOINT:
  impl_->belt_joint_ = _model->GetJoint("belt_joint");

  if (!impl_->belt_joint_) {
    RCLCPP_ERROR(impl_->ros_node_->get_logger(), "Belt joint not found, unable to start conveyor plugin.");
    return;
  }

  // Set velocity (m/s)
  impl_->max_velocity_ = _sdf->GetElement("max_velocity")->Get<double>();

  // Set limit (m)
  impl_->limit_ = impl_->belt_joint_->UpperLimit();

  // Create status publisher
  impl_->status_pub_ = impl_->ros_node_->create_publisher<conveyorbelt_msgs::msg::ConveyorBeltState>("CONVEYORSTATE", 10);
  impl_->status_msg_.enabled = false;
  impl_->status_msg_.power = 0;

  // REGISTER ConveyorBelt SERVICE:
  impl_->enable_service_ =
    impl_->ros_node_->create_service<conveyorbelt_msgs::srv::ConveyorBeltControl>(
    "CONVEYORPOWER", std::bind(
      &ROS2ConveyorBeltPluginPrivate::SetConveyorPower, impl_.get(),
      std::placeholders::_1, std::placeholders::_2));

  double publish_rate = _sdf->GetElement("publish_rate")->Get<double>();
  impl_->update_ns_ = int((1/publish_rate) * 1e9);

  impl_->last_publish_time_ = impl_->ros_node_->get_clock()->now();

  // Create a connection so the OnUpdate function is called at every simulation iteration. 
  impl_->update_connection_ = gazebo::event::Events::ConnectWorldUpdateBegin(
    std::bind(&ROS2ConveyorBeltPluginPrivate::OnUpdate, impl_.get()));

  RCLCPP_INFO(impl_->ros_node_->get_logger(), "GAZEBO ConveyorBelt plugin loaded successfully.");
}

void ROS2ConveyorBeltPluginPrivate::OnUpdate()
{
  belt_joint_->SetVelocity(0, belt_velocity_);

  double belt_position = belt_joint_->Position(0);

  if (belt_position >= limit_){
    belt_joint_->SetPosition(0, 0);
  }

  // Publish status at rate
  rclcpp::Time now = ros_node_->get_clock()->now();
  if (now - last_publish_time_ >= rclcpp::Duration(0, update_ns_)) {
    PublishStatus();
    last_publish_time_ = now;
  }
    
}

void ROS2ConveyorBeltPluginPrivate::SetConveyorPower(
  conveyorbelt_msgs::srv::ConveyorBeltControl::Request::SharedPtr req,
  conveyorbelt_msgs::srv::ConveyorBeltControl::Response::SharedPtr res)
{
  res->success = false;
  if (req->power >= 0 && req->power <= 100) {
    power_ = req->power;
    belt_velocity_ = max_velocity_ * (power_ / 100);
    res->success = true;
  }
  else{
    RCLCPP_WARN(ros_node_->get_logger(), "Conveyor power must be between 0 and 100.");
  }
}

void ROS2ConveyorBeltPluginPrivate::PublishStatus(){
  status_msg_.power = power_;

  if (power_ > 0)
    status_msg_.enabled = true;
  else {
    status_msg_.enabled = false;
  }

  status_pub_->publish(status_msg_);
}

GZ_REGISTER_MODEL_PLUGIN(ROS2ConveyorBeltPlugin)
}  // namespace gazebo_ros