#ifndef ROS2_CONVEYORBELT_PLUGIN_HPP_
#define ROS2_CONVEYORBELT_PLUGIN_HPP_

#include <gazebo/common/Plugin.hh>
#include <memory>

namespace gazebo_ros
{

class ROS2ConveyorBeltPluginPrivate;

class ROS2ConveyorBeltPlugin : public gazebo::ModelPlugin
{
public:
  /// Constructor:
  ROS2ConveyorBeltPlugin();

  /// Destructor:
  virtual ~ROS2ConveyorBeltPlugin();

  // LOAD plugin:
  void Load(gazebo::physics::ModelPtr _model, sdf::ElementPtr _sdf) override;

private:

  std::unique_ptr<ROS2ConveyorBeltPluginPrivate> impl_;
};

}  // namespace gazebo_ros

#endif  // ROS2_CONVEYORBELT_PLUGIN_HPP_