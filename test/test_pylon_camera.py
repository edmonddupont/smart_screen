from pypylon import pylon
import cv2

def main():
    try:
        devices = pylon.TlFactory.GetInstance().EnumerateDevices()
        print("Number of devices found:", len(devices))
        for d in devices:
            print(d.GetModelName(), d.GetSerialNumber())
            
        # Get camera instance
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        camera.Open()
        print("Camera opened:", camera.GetDeviceInfo().GetModelName())

        # Grab one image
        camera.StartGrabbingMax(1)
        grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grab_result.GrabSucceeded():
            print("Image grabbed successfully.")
            img = grab_result.Array

            # Optional: Convert Bayer to BGR
            img_bgr = cv2.cvtColor(img, cv2.COLOR_BAYER_RG2BGR)

            cv2.imshow("Test Frame", img_bgr)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Grab failed.")

        grab_result.Release()
        camera.Close()

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
