using WindowsInput;
using WindowsInput.Native;

namespace AutoClicker {
  class Client {
    doClick(Point point) {
      var defaultCursor = new Point()
      {
        X = Cursor.Position.X,
        Y = Cursor.Position.Y
      };

      var sim = new InputSimulator();

      Cursor.Position = point;
      sim.Mouse.LeftButtonClick();
      Cursor.Position = defaultCursor;
    }
  }
}

var client = new Client()l

client.doClick(new Point(100, 200));